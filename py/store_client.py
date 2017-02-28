from __future__ import print_function

import grpc

import store_pb2
from tracer_interceptor import TracerInterceptor
from interceptor_channel import InterceptorChannel


def run():
  tracer = None
  tracer_interceptor = TracerInterceptor(tracer)
  channel = grpc.insecure_channel('localhost:50051')
  channel = InterceptorChannel(channel, tracer_interceptor)
  stub = store_pb2.StoreStub(channel)
  response = stub.GetQuantity(store_pb2.QuantityRequest(item_id=51))
  print("Quantity: " + str(response.quantity))


if __name__ == '__main__':
  run()
