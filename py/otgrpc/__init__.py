import abc

import six


class ActiveSpanSource(six.with_metaclass(abc.ABCMeta)):
    """Provides a way to customize how the active span is determined."""

    @abc.abstractmethod
    def get_active_span(self):
        """Identifies the active span.

        Returns:
          An object that implements the opentracing.Span interface.
        """


def open_tracing_client_interceptor(tracer, active_span_source=None):
    """Creates a client-side interceptor that can be use with gRPC to add
         OpenTracing information.

    Args:
      tracer: An object implmenting the opentracing.Tracer interface.
      active_span_source: An optional ActiveSpanSource to customize how the
        active span is determined.

    Returns:
      A client-side interceptor object.
    """
    from otgrpc import _client
    return _client.OpenTracingClientInterceptor(tracer, active_span_source)


def open_tracing_server_interceptor(tracer):
    """Creates a server-side interceptor that can be use with gRPC to add
         OpenTracing information.

    Args:
      tracer: An object implmenting the opentracing.Tracer interface.

    Returns:
      A server-side interceptor object.
    """
    from otgrpc import _server
    return _server.OpenTracingServerInterceptor(tracer)
