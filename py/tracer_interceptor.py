import opentracing
# Implementation for interceptors that implement open tracing. The plan is to
# eventually check these into
# https://github.com/grpc-ecosystem/grpc-opentracing


def inject_span_context(tracer, span_context, metadata):
    attributes = {}
    tracer.inject(span_context, opentracing.Format.HTTP_HEADERS, attributes)
    metadata = () if metadata is None else tuple(metadata)
    return metadata + tuple(attributes.iteritems())


class OpenTracingClientInterceptor(object):
    def __init__(self, tracer):
        self.tracer = tracer

    def __call__(self, method, request, metadata, invoker):
        # TODO: need a method to get the active parent span
        with self.tracer.start_span(method) as span:
            metadata = inject_span_context(self.tracer, span.context, metadata)
            return invoker(request, metadata)


class OpenTracingServerInterceptor(object):
    def __call__(self, request, servicer_context, invoker):
        print 'before response'
        print 'metadata=' + str(servicer_context.invocation_metadata())
        response = invoker(request, servicer_context)
        print 'after response'
        return response
