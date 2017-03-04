from grpc_tools import protoc

protoc.main(
    (
        '',
        '-I../proto2',
        '--python_out=.',
        '--grpc_python_out=.',
        '../proto2/store.proto'
    )
)
