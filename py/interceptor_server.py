# An implementation for server-side interceptors for gRPC Python.
# The plan is to eventually check in this code somewhere in the gRPC source as
# a PR for https://github.com/grpc/grpc/issues/8767

import grpc
import collections


UnaryServerInfo = collections.namedtuple('UnaryServerInfo', 'full_method')


class InterceptorRpcMethodHandler(grpc.RpcMethodHandler):
    def __init__(self, rpc_method_handler, method, interceptor):
        self.rpc_method_handler = rpc_method_handler
        self.method = method
        self.interceptor = interceptor

    @property
    def request_streaming(self):
        return self.rpc_method_handler.request_streaming

    @property
    def response_streaming(self):
        return self.rpc_method_handler.response_streaming

    @property
    def request_deserializer(self):
        return self.rpc_method_handler.request_deserializer

    @property
    def response_serializer(self):
        return self.rpc_method_handler.response_serializer

    @property
    def unary_unary(self):
        def adaptation(request, servicer_context):
            def handler(request):
                return self.rpc_method_handler.unary_unary(request,
                                                           servicer_context)
            return self.interceptor(request,
                                    servicer_context.invocation_metadata(),
                                    UnaryServerInfo(self.method),
                                    handler)
        return adaptation

    @property
    def unary_stream(self):
        return self.rpc_method_handler.unary_stream

    @property
    def stream_unary(self):
        return self.rpc_method_handler.stream_unary

    @property
    def stream_stream(self):
        return self.rpc_method_handler.stream_stream


class InterceptorGenericRpcHandler(grpc.GenericRpcHandler):
    def __init__(self, generic_rpc_handler, interceptor):
        self.generic_rpc_handler = generic_rpc_handler
        self.interceptor = interceptor

    def service(self, handler_call_details):
        result = self.generic_rpc_handler.service(handler_call_details)
        if result:
            result = InterceptorRpcMethodHandler(result,
                                                 handler_call_details.method,
                                                 self.interceptor)
        return result


class InterceptorServer(grpc.Server):
    def __init__(self, server, interceptor):
        self.server = server
        self.interceptor = interceptor

    def add_generic_rpc_handlers(self, generic_rpc_handlers):
        generic_rpc_handlers = [
          InterceptorGenericRpcHandler(generic_rpc_handler, self.interceptor)
          for generic_rpc_handler in generic_rpc_handlers]
        self.server.add_generic_rpc_handlers(generic_rpc_handlers)

    def add_insecure_port(self, *args, **kwargs):
        self.server.add_insecure_port(*args, **kwargs)

    def add_secure_port(self, *args, **kwargs):
        self.server.add_secure_port(*args, **kwargs)

    def start(self):
        self.server.start()

    def stop(self, *args, **kwargs):
        self.server.stop(*args, **kwargs)
