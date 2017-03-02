import six
import abc


class UnaryServerInfo(six.with_metaclass(abc.ABCMeta)):
    """UnaryServerInfo consists of various information about a unary RPC on
         server side.

    Attributes:
      full_method: A string of the full RPC method, i.e.,
        /package.service/method.
    """


# TODO: support multiple interceptor arguments
def intercept_channel(channel, interceptor):
    from grpcext import _interceptor
    return _interceptor.intercept_channel(channel, interceptor)


# TODO: support multiple interceptor arguments
def intercept_server(server, interceptor):
    from grpcext import _interceptor
    return _interceptor.intercept_server(server, interceptor)
