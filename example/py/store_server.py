# A OpenTraced server for a Python service that implements the store interface.
from concurrent import futures
import time
import sys

import grpc

import store_pb2
from grpcext import intercept_server
from otgrpc import open_tracing_server_interceptor
import lightstep
import argparse

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Store(store_pb2.StoreServicer):
    def GetQuantity(self, request, context):
        return store_pb2.QuantityResponse(quantity=301)

    def StocksItems(self, request_iterator, context):
        return store_pb2.Bool(value=True)


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access_token', help='LightStep Access Token')
    parser.add_argument(
        '--log_payloads', action='store_true',
        help='log request/response objects to open-tracing spans')
    args = parser.parse_args()
    if not args.access_token:
        print('You must specify access_token')
        sys.exit(-1)

    tracer = lightstep.Tracer(component_name='python.store-server',
                              access_token=args.access_token)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    tracer_interceptor = open_tracing_server_interceptor(
                              tracer,
                              log_payloads=args.log_payloads)
    server = intercept_server(server, tracer_interceptor)

    store_pb2.add_StoreServicer_to_server(Store(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

    tracer.flush()

if __name__ == '__main__':
    serve()
