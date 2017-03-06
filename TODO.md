* **Add utility functions that can chain multiple interceptors.** The plan in to make something similar to this [function](http://www.grpc.io/grpc-java/javadoc/io/grpc/ClientInterceptors.html#intercept-io.grpc.Channel-java.util.List-) for the client-side and this [function](http://www.grpc.io/grpc-java/javadoc/io/grpc/ServerInterceptors.html#intercept-io.grpc.ServerServiceDefinition-io.grpc.ServerInterceptor...-) on the server-side.

* **Move interceptor code into the gRPC repository.**

* **Add coverage for the interceptor code into gRPC’s unit testing framework.** The tests will need to fit somewhere in [here](https://github.com/grpc/grpc/tree/master/src/python/grpcio_tests/tests).

* **Move the tracer interceptor code into the grpc-ecosystem repository.**

* **Add test coverage for the tracer interceptors.**

