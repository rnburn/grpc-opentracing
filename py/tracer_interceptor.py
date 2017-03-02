# Implementation for interceptors that implement open tracing. The plan is to
# eventually check these into
# https://github.com/grpc-ecosystem/grpc-opentracing

import opentracing


def inject_span_context(tracer, span_context, metadata):
    headers = {}
    tracer.inject(span_context, opentracing.Format.HTTP_HEADERS, headers)
    metadata = () if metadata is None else tuple(metadata)
    return metadata + tuple(headers.iteritems())


class OpenTracingClientInterceptor(object):
    def __init__(self, tracer):
        self.tracer = tracer

    def __call__(self, method, request, metadata, invoker):
        # TODO: need a method to get the active parent span
        with self.tracer.start_span(method) as span:
            metadata = inject_span_context(self.tracer, span.context, metadata)
            return invoker(request, metadata)


def start_server_span(tracer, metadata, method):
    span_context = None
    tags = None
    try:
        if metadata:
            span_context = tracer.extract(opentracing.Format.HTTP_HEADERS,
                                          dict(metadata))
    except (opentracing.InvalidCarrierException,
            opentracing.SpanContextCorruptedException) as e:
        tags = {'Extract failed': str(e)}
    return tracer.start_span(operation_name=method, child_of=span_context,
                             tags=tags)


class OpenTracingServerInterceptor(object):
    def __init__(self, tracer):
        self.tracer = tracer

    def __call__(self, request, metadata, server_info, handler):
        with start_server_span(self.tracer, metadata, server_info.full_method):
            return handler(request)
