import opentracing


def _inject_span_context(tracer, span_context, metadata):
    headers = {}
    tracer.inject(span_context, opentracing.Format.HTTP_HEADERS, headers)
    metadata = () if metadata is None else tuple(metadata)
    return metadata + tuple(headers.iteritems())


class OpenTracingClientInterceptor(object):
    def __init__(self, tracer, active_span_source):
        self._tracer = tracer
        self._active_span_source = active_span_source

    def __call__(self, method, request, metadata, invoker):
        active_span_context = None
        if self._active_span_source:
            active_span_context = \
                    self._active_span_source.get_active_span().context
        with self._tracer.start_span(operation_name=method,
                                     child_of=active_span_context) as span:
            metadata = _inject_span_context(self._tracer, span.context,
                                            metadata)
            return invoker(request, metadata)
