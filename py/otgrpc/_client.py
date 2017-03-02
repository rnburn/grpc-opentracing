import opentracing


def _inject_span_context(tracer, span_context, metadata):
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
            metadata = _inject_span_context(self.tracer, span.context,
                                            metadata)
            return invoker(request, metadata)
