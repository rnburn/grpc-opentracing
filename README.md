This is an initial staging area to develop two projects.

1. An implementation of interceptors for the Python version of gRPC. (This [ticket](https://github.com/grpc/grpc/issues/8767)).
2. Python gRPC interceptors that implement open-tracing.

The code organized in the following way:

py/ <- A python implementation of gRPC interceptors and a OpenTracing interceptors
example/proto/ <- A simple proto file describing a service that returns a quantity for a given itemid.
example/go/ <- A go implementation of the service using OpenTracing
example/py/ <- A Python implementation of the service using OpenTracing
