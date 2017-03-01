# A OpenTraced server for a Python service that implements the store interface.
from concurrent import futures
import time

import grpc

import store_pb2
from tracer_interceptor import OpenTracingServerInterceptor
from interceptor_server import InterceptorServer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Store(store_pb2.StoreServicer):
    def GetQuantity(self, request, context):
        return store_pb2.QuantityResponse(quantity=301)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    tracer_interceptor = OpenTracingServerInterceptor()
    server = InterceptorServer(server, tracer_interceptor)

    store_pb2.add_StoreServicer_to_server(Store(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
