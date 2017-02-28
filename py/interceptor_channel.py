# An implementation for client-side interceptors for gRPC Python.
# The plan is to eventually check in this code somewhere in the gRPC source as
# a PR for https://github.com/grpc/grpc/issues/8767

import grpc


class InterceptorUnaryUnaryMultiCallable(grpc.UnaryUnaryMultiCallable):
    def __init__(self, base_callable, interceptor):
        self.base_callable = base_callable
        self.interceptor = interceptor

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        def invoker(request, metadata):
            return self.base_callable(request, timeout, metadata, credentials)
        return self.interceptor(request, metadata, invoker)

    def with_call(self, *args, **kwargs):
        self.base_callable.with_call(*args, **kwargs)

    def future(self, *args, **kwargs):
        self.base_callable.future(*args, **kwargs)


class InterceptorChannel(grpc.Channel):
    def __init__(self, channel, interceptor):
        self.channel = channel
        self.interceptor = interceptor

    def subscribe(self, *args, **kwargs):
        self.channel.subscribe(*args, **kwargs)

    def unsubscribe(self, *args, **kwargs):
        self.channel.unsubscribe(*args, **kwargs)

    def unary_unary(self, *args, **kwargs):
        base_callable = self.channel.unary_unary(*args, **kwargs)
        return InterceptorUnaryUnaryMultiCallable(
            base_callable, self.interceptor)

    def unary_stream(self, *args, **kwargs):
        return self.channel.unary_stream(*args, **kwargs)

    def stream_unary(self, *args, **kwargs):
        return self.channel.stream_unary(*args, **kwargs)

    def stream_stream(self, *args, **kwargs):
        return self.channel.stream_stream(*args, **kwargs)
