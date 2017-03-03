import sys
import logging

import grpc
import grpcext
import opentracing


def _inject_span_context(tracer, span, metadata):
    headers = {}
    try:
        tracer.inject(span.context, opentracing.Format.HTTP_HEADERS, headers)
    except (opentracing.UnsupportedFormatException,
            opentracing.InvalidCarrierException,
            opentracing.SpanContextCorruptedException) as e:
        logging.exception('tracer.inject() failed')
        span.log_kv({'event': 'error', 'error.object': e})
        return metadata
    metadata = () if metadata is None else tuple(metadata)
    return metadata + tuple(headers.iteritems())


class OpenTracingClientInterceptor(grpcext.UnaryClientInterceptor,
                                   grpcext.StreamClientInterceptor):
    def __init__(self, tracer, active_span_source, log_payloads):
        self._tracer = tracer
        self._active_span_source = active_span_source
        self._log_payloads = log_payloads

    def start_span(self, method):
        active_span_context = None
        if self._active_span_source:
            active_span_context = \
                    self._active_span_source.get_active_span().context
        # TODO: add peer.hostname, peer.ipv4, and other RPC fields that are
        # mentioned on
        # https://github.com/opentracing/specification/blob/master/semantic_conventions.md
        tags = {
            'component': 'grpc',
            'span.kind': 'client'
        }
        return self._tracer.start_span(operation_name=method,
                                       child_of=active_span_context,
                                       tags=tags)

    def intercept_unary(self, method, request, metadata, invoker):
        with self.start_span(method) as span:
            metadata = _inject_span_context(self._tracer, span, metadata)
            response = None
            if self._log_payloads:
                span.log_kv({'request': request})
            try:
                response = invoker(request, metadata)
            except:
                e = sys.exc_info()[0]
                span.set_tag('error', True)
                span.log_kv({'event': 'error', 'error.object': e})
                raise
            # if the RPC is called asynchronously, don't log responses
            if self._log_payloads and not isinstance(response, grpc.Future):
                span.log_kv({'response': response})
            return response

    def intercept_stream(self, metadata, client_info, invoker):
        return invoker(metadata)
