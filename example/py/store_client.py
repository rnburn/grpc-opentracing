# A OpenTraced client for a Python service that implements the store interface.
from __future__ import print_function

import grpc
import sys

import store_pb2
from grpcext import intercept_channel
from otgrpc import open_tracing_client_interceptor
import lightstep
import argparse


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access_token', help='LightStep Access Token')
    parser.add_argument('--call_async', action='store_true',
                        help='call the service asynchronously')
    parser.add_argument(
        '--log_payloads', action='store_true',
        help='log request/response objects to open-tracing spans')
    args = parser.parse_args()
    if not args.access_token:
        print('You must specify access_token')
        sys.exit(-1)

    tracer = lightstep.Tracer(component_name='python.store-client',
                              access_token=args.access_token)
    tracer_interceptor = open_tracing_client_interceptor(
                                                tracer, 
                                                log_payloads=args.log_payloads)
    channel = grpc.insecure_channel('localhost:50051')
    channel = intercept_channel(channel, tracer_interceptor)
    stub = store_pb2.StoreStub(channel)

    request = store_pb2.QuantityRequest(item_id=51)
    response = None
    if args.call_async:
        response_future = stub.GetQuantity.future(request)
        response = response_future.result()
    else:
        response = stub.GetQuantity(request)
    print('Quantity: ' + str(response.quantity))

    requests = [store_pb2.Item(item_id=21), store_pb2.Item(item_id=33)]
    response = stub.StocksItems(iter(requests))
    print('Stocks Items: ' + str(response.value))

    tracer.flush()


if __name__ == '__main__':
    run()
