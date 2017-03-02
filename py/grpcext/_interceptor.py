import grpc
import collections


class _UnaryServerInfo(
    collections.namedtuple(
        '_UnaryServerInfo', ('full_method',))):
    pass


class _InterceptorUnaryUnaryMultiCallable(grpc.UnaryUnaryMultiCallable):
    def __init__(self, method, base_callable, interceptor):
        self._method = method
        self._base_callable = base_callable
        self._interceptor = interceptor

    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        def invoker(request, metadata):
            return self._base_callable(request, timeout, metadata, credentials)
        return self._interceptor(self._method, request, metadata, invoker)

    def with_call(self, *args, **kwargs):
        self._base_callable.with_call(*args, **kwargs)

    def future(self, *args, **kwargs):
        self._base_callable.future(*args, **kwargs)


class _InterceptorUnaryStreamMultiCallable(grpc.UnaryStreamMultiCallable):
    def __call__(self, request, timeout=None, metadata=None, credentials=None):
        pass


class _InterceptorStreamUnaryMultiCallable(grpc.StreamUnaryMultiCallable):
    def __call__(
      self, request_iterator, timeout=None, metadata=None, credentials=None):
        pass


class StreamStreamMultiCallable(grpc.StreamStreamMultiCallable):
    def __call__(
      self, request_iterator, timeout=None, metadata=None, credentials=None):
        pass


class _InterceptorChannel(grpc.Channel):
    def __init__(self, channel, interceptor):
        self._channel = channel
        self._interceptor = interceptor

    def subscribe(self, *args, **kwargs):
        self._channel.subscribe(*args, **kwargs)

    def unsubscribe(self, *args, **kwargs):
        self._channel.unsubscribe(*args, **kwargs)

    def unary_unary(
      self, method, request_serializer=None, response_deserializer=None):
        base_callable = self._channel.unary_unary(
          method, request_serializer, response_deserializer)
        return _InterceptorUnaryUnaryMultiCallable(
            method, base_callable, self._interceptor)

    def unary_stream(self, *args, **kwargs):
        return self._channel.unary_stream(*args, **kwargs)

    def stream_unary(self, *args, **kwargs):
        return self._channel.stream_unary(*args, **kwargs)

    def stream_stream(self, *args, **kwargs):
        return self._channel.stream_stream(*args, **kwargs)


# TODO: support multiple interceptor arguments
def intercept_channel(channel, interceptor):
    return _InterceptorChannel(channel, interceptor)


class _InterceptorRpcMethodHandler(grpc.RpcMethodHandler):
    def __init__(self, rpc_method_handler, method, interceptor):
        self._rpc_method_handler = rpc_method_handler
        self._method = method
        self._interceptor = interceptor

    @property
    def request_streaming(self):
        return self._rpc_method_handler.request_streaming

    @property
    def response_streaming(self):
        return self._rpc_method_handler.response_streaming

    @property
    def request_deserializer(self):
        return self._rpc_method_handler.request_deserializer

    @property
    def response_serializer(self):
        return self._rpc_method_handler.response_serializer

    @property
    def unary_unary(self):
        def adaptation(request, servicer_context):
            def handler(request):
                return self._rpc_method_handler.unary_unary(request,
                                                            servicer_context)
            return self._interceptor(request,
                                     servicer_context.invocation_metadata(),
                                     _UnaryServerInfo(self._method),
                                     handler)
        return adaptation

    @property
    def unary_stream(self):
        return self._rpc_method_handler.unary_stream

    @property
    def stream_unary(self):
        return self._rpc_method_handler.stream_unary

    @property
    def stream_stream(self):
        return self._rpc_method_handler.stream_stream


class _InterceptorGenericRpcHandler(grpc.GenericRpcHandler):
    def __init__(self, generic_rpc_handler, interceptor):
        self.generic_rpc_handler = generic_rpc_handler
        self._interceptor = interceptor

    def service(self, handler_call_details):
        result = self.generic_rpc_handler.service(handler_call_details)
        if result:
            result = _InterceptorRpcMethodHandler(result,
                                                  handler_call_details.method,
                                                  self._interceptor)
        return result


class _InterceptorServer(grpc.Server):
    def __init__(self, server, interceptor):
        self._server = server
        self._interceptor = interceptor

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        generic_rpc_handlers = [
          _InterceptorGenericRpcHandler(generic_rpc_handler, self._interceptor)
          for generic_rpc_handler in generic_rpc_handlers]
        self._server.add_generic_rpc_handlers(generic_rpc_handlers)

    def add_insecure_port(self, *args, **kwargs):
        self._server.add_insecure_port(*args, **kwargs)

    def add_secure_port(self, *args, **kwargs):
        self._server.add_secure_port(*args, **kwargs)

    def start(self):
        self._server.start()

    def stop(self, *args, **kwargs):
        self._server.stop(*args, **kwargs)


# TODO: support multiple interceptor arguments
def intercept_server(server, interceptor):
    return _InterceptorServer(server, interceptor)
