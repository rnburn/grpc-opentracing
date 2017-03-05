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

def execute_command(rpc_executer, command, command_arguments):
    via = 'functor'
    if len(command_arguments) > 1 and command_arguments[0] == '--via':
        via = command_arguments[1]
        if via not in ('functor', 'with_call', 'future'):
            print('invalid --via option')
            return
        command_arguments = command_arguments[2:]
    if command == 'stock_item':
        requests = [store_pb2.AddItemRequest(name=name) 
                        for name in command_arguments]
        if len(requests) != 1:
            print('must input a single element')
            return
        request = requests[0]
        rpc_executer('AddItem', request, via)
    elif command == 'stock_items':
        requests = [store_pb2.AddItemRequest(name=name) 
                        for name in command_arguments]
        if not requests:
            print('must input at least one item')
            return
        rpc_executer('AddItems', iter(requests), via)
    elif command == 'sell_item':
        requests = [store_pb2.RemoveItemRequest(name=name)
                        for name in command_arguments]
        if len(requests) != 1:
            print('must input a single element')
            return
        request = requests[0]
        response = rpc_executer('RemoveItem', request, via)
        if not response.was_successful:
            print('unable to sell')
    elif command == 'sell_items':
        requests = [store_pb2.RemoveItemRequest(name=name)
                        for name in command_arguments]
        if not requests:
            print('must input at least one item')
            return
        response = rpc_executer('RemoveItems', iter(requests), via)
        if not response.was_successful:
            print('unable to sell')
    elif command == 'inventory':
        if via != 'functor':
            print('inventory can only be called via functor')
            return
        request = store_pb2.Empty()
        result = rpc_executer('ListInventory', request, via)
        for query in result:
            print(query.name, '\t', query.count)
    elif command == 'query_item':
        requests = [store_pb2.QueryItemRequest(name=name) 
                        for name in command_arguments]
        if len(requests) != 1:
            print('must input a single element')
            return
        request = requests[0]
        query = rpc_executer('QueryQuantity', request, via)
        print(query.name, '\t', query.count)
    elif command == 'query_items':
        if via != 'functor':
            print('query_items can only be called via functor')
            return
        requests = [store_pb2.QueryItemRequest(name=name) 
                        for name in command_arguments]
        if not requests:
            print('must input at least one item')
            return
        result = rpc_executer('QueryQuantities', iter(requests), via)
        for query in result:
            print(query.name, '\t', query.count)
    else:
        print('Unknown command: "%s"' % command)

instructions = \
"""Enter commands to interact with the store service:

    stock_item     Stock a single item.
    stock_items    Stock one or more items.
    sell_item      Sell a single item.
    sell_items     Sell one or more items.
    inventory      List the store's inventory.
    query_item     Query the inventory for a single item.
    query_items    Query the inventory for one or more items.

You can also optionally provide a --via argument to instruct the RPC to be
initiated via either the functor, with_call, or future method.

Example:
    > stock_item apple
    > stock_items --via future apple milk
    > inventory
    apple   2
    milk    1
"""

def read_and_execute(rpc_executer):
    print(instructions)
    while True:
        try:
            line = raw_input('> ')
            components = line.split()
            if not components:
                continue
            command = components[0]
            command_arguments = components[1:]
            execute_command(rpc_executer, command, command_arguments)
        except EOFError:
            break


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--access_token', help='LightStep Access Token')
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

    tracer.flush()


if __name__ == '__main__':
    run()
