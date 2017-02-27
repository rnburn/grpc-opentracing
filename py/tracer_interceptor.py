class TracerInterceptor(object):
    def __init__(self, tracer):
        self.tracer = tracer

    def __call__(self, request, metadata, invoker):
        print "before call to server"
        response = invoker(request, metadata)
        print "after call to server"
        return response
