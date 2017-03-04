# A OpenTraced client for a Python service that implements the store interface.
from __future__ import print_function

import grpc
import sys

import store_pb2
from grpcext import intercept_channel
from otgrpc import open_tracing_client_interceptor
import lightstep
import argparse
import collections

class RpcExecuter(object):
    def __init__(self, stub):
        self._stub = stub

    def __call__(self, method, request_or_iter, call_method):
        if call_method == 'future':
            result = getattr(self._stub, method).future(request_or_iter)
            return result.result()
        elif call_method == 'with_call':
            return getattr(self._stub, method).with_call(request_or_iter)[0]
        else:
            return getattr(self._stub, method)(request_or_iter)

def read_and_execute(rpc_executer):
    parser = argparse.ArgumentParser()
    parser.add_argument('--via', choices=('functor', 'with_call', 'future'),
                        default='functor')
    parser.add_argument('command_arguments', nargs='*')
    while True:
        try:
            line = raw_input('> ')
            components = line.split()
            if not components:
                continue
            command = components[0]
            arguments = parser.parse_args(components[1:])
            command_arguments = arguments.command_arguments
            if command == 'stock':
                method = 'AddItem'
                requests = [store_pb2.AddItemRequest(name=name) 
                                for name in command_arguments]
                if not requests:
                    print('must input at least one item')
                    continue
                request_or_iter = requests[0]
                if len(requests) > 1:
                    method = 'AddItems'
                    request_or_iter = iter(requests)
                rpc_executer(method, request_or_iter, arguments.via)
            elif command == 'sell':
                method = 'RemoveItem'
                requests = [store_pb2.RemoveItemRequest(name=name)
                                for name in command_arguments]
                if not requests:
                    print('must input at least one item')
                    continue
                request_or_iter = requests[0]
                if len(requests) > 1:
                    method = 'RemoveItems'
                    request_or_iter = iter(requests)
                response = rpc_executer(method, request_or_iter, arguments.via)
                if not response.was_successful:
                    print('unable to sell')
            elif command == 'list':
                method = 'ListInventory'
                request = store_pb2.Empty()
                response = list(rpc_executer(method, request, arguments.via))
                for query in response:
                    print(query.name, ': ', query.count)
            elif command == 'query':
                method = 'QueryQuantity'
                requests = [store_pb2.QueryItemRequest(name=name) 
                                for name in command_arguments]
                if not requests:
                    print('must input at least one item')
                    continue
                request_or_iter = requests[0]
                if len(requests) > 1:
                    method = 'QueryQuantities'
                    request_or_iter = iter(requests)
                response = rpc_executer(method, request_or_iter, arguments.via)
                if isinstance(response, collections.Iterable):
                    response = list(response)
                else:
                    response = [response]
                for query in response:
                    print(query.name, '\t', query.count)
            else:
                print('Unknown command: "%s"' % command)
            # print(command)
            # print(arguments.command_arguments)
        except EOFError:
            break


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

    read_and_execute(RpcExecuter(stub))
    # request = store_pb2.QuantityRequest(item_id=51)
    # response = None
    # if args.call_async:
    #     response_future = stub.GetQuantity.future(request)
    #     response = response_future.result()
    # else:
    #     response = stub.GetQuantity(request)
    # print('Quantity: ' + str(response.quantity))

    # requests = [store_pb2.Item(item_id=21), store_pb2.Item(item_id=33)]
    # response = stub.StocksItems(iter(requests))
    # print('Stocks Items: ' + str(response.value))

    tracer.flush()


if __name__ == '__main__':
    run()
