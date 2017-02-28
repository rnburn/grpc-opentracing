# A OpenTraced client for a Python service that implements the store interface.
from __future__ import print_function

import grpc

import store_pb2
from tracer_interceptor import OpenTracingClientInterceptor
from interceptor_channel import InterceptorChannel
from opentracing import Tracer


def run():
    tracer = Tracer()
    tracer_interceptor = OpenTracingClientInterceptor(tracer)
    channel = grpc.insecure_channel('localhost:50051')
    channel = InterceptorChannel(channel, tracer_interceptor)
    stub = store_pb2.StoreStub(channel)
    response = stub.GetQuantity(store_pb2.QuantityRequest(item_id=51))
    print('Quantity: ' + str(response.quantity))


if __name__ == '__main__':
    run()
