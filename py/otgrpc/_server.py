import sys
import logging

import grpcext
import opentracing


def _start_server_span(tracer, metadata, method):
    span_context = None
    error = None
    try:
        if metadata:
            span_context = tracer.extract(opentracing.Format.HTTP_HEADERS,
                                          dict(metadata))
    except (opentracing.UnsupportedFormatException,
            opentracing.InvalidCarrierException,
            opentracing.SpanContextCorruptedException) as e:
        logging.exception('tracer.extract() failed')
        error = e
    # TODO: add peer.hostname, peer.ipv4, and other RPC fields that are
    # mentioned on
    # https://github.com/opentracing/specification/blob/master/semantic_conventions.md
    tags = {
        'component': 'grpc',
        'span.kind': 'server'
    }
    span = tracer.start_span(operation_name=method, child_of=span_context,
                             tags=tags)
    if error is not None:
        span.log_kv({'event': 'error', 'error.object': error})
    return span


class OpenTracingServerInterceptor(grpcext.UnaryServerInterceptor,
                                   grpcext.StreamServerInterceptor):
    def __init__(self, tracer, log_payloads):
        self._tracer = tracer
        self._log_payloads = log_payloads

    def intercept_unary(self, request, metadata, server_info, handler):
        with _start_server_span(self._tracer, metadata,
                                server_info.full_method) as span:
            response = None
            if self._log_payloads:
                span.log_kv({'request': request})
            try:
                response = handler(request)
            except:
                e = sys.exc_info()[0]
                span.set_tag('error', True)
                span.log_kv({'event': 'error', 'error.object': e})
                raise
            if self._log_payloads:
                span.log_kv({'response': response})
            return response

    # For RPCs that stream responses, the result can be a generator. To record
    # the span across the generated responses and detect any errors, we wrap the
    # result in a new generator that yields the response values.
    def _intercept_server_stream(self, metadata, server_info, handler):
        with _start_server_span(self._tracer, metadata,
                                server_info.full_method) as span:
            try:
                result = handler()
                for response in result:
                    yield response
            except:
                e = sys.exc_info()[0]
                span.set_tag('error', True)
                span.log_kv({'event': 'error', 'error.object': e})
                raise

    def intercept_stream(self, metadata, server_info, handler):
        if server_info.is_server_stream:
            return self._intercept_server_stream(metadata, server_info, handler)
        with _start_server_span(self._tracer, metadata,
                                server_info.full_method) as span:
            try:
                return handler()
            except:
                e = sys.exc_info()[0]
                span.set_tag('error', True)
                span.log_kv({'event': 'error', 'error.object': e})
                raise
