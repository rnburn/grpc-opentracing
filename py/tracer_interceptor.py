# Implementation for interceptors that implement open tracing. The plan is to
# eventually check these into
# https://github.com/grpc-ecosystem/grpc-opentracing


class OpenTracingClientInterceptor(object):
    def __init__(self, tracer):
        self.tracer = tracer

    def __call__(self, method, request, metadata, invoker):
        # TODO: need a method to get the active parent span
        with self.tracer.start_span(method):
            # TODO: inject the context into metadata
            return invoker(request, metadata)
