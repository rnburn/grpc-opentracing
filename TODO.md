* **Add a tracer interceptor for synchronous calls on the server-side.**

* **Add the ability to customize the method of obtaining a parent span in client-side interceptors.**

* **Redesign interceptor interface to support asynchronous and batch RPC calls.**
An interceptor interface like
```python
  def __call__(self, method, request, metadata, invoker):
    …
```
won’t work for the batch versions where multiple requests are sent at once. I’ll probably do something similar to what’s done for Go which distinguishes between [unary](https://godoc.org/google.golang.org/grpc#WithUnaryInterceptor) and [stream](https://godoc.org/google.golang.org/grpc#WithStreamInterceptor) interceptors. We may also want some way to distinguish an intercepted synchronous call from an intercepted asynchronous call.

* **Add interceptors for the async and batch RPC calls for both the client-side and the server-side.**

* **Add utility functions that can chain multiple interceptors.** The plan in to make something similar to this [function](http://www.grpc.io/grpc-java/javadoc/io/grpc/ClientInterceptors.html#intercept-io.grpc.Channel-java.util.List-) for the client-side and this [function](http://www.grpc.io/grpc-java/javadoc/io/grpc/ServerInterceptors.html#intercept-io.grpc.ServerServiceDefinition-io.grpc.ServerInterceptor...-) on the server-side.

* **Move interceptor code into the gRPC repository.**

* **Add coverage for the interceptor code into gRPC’s unit testing framework.** The tests will need to fit somewhere in [here](https://github.com/grpc/grpc/tree/master/src/python/grpcio_tests/tests).

* **Move the tracer interceptor code into the grpc-ecosystem repository.**

* **Add test coverage for the tracer interceptors.**

