import opentracing


def _start_server_span(tracer, metadata, method):
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
        self._tracer = tracer

    def __call__(self, request, metadata, server_info, handler):
        with _start_server_span(self._tracer, metadata,
                                server_info.full_method):
            return handler(request)
