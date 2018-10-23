### gRPC repo

here we need to store the protobuf and gRPC code

to build Proto, run:

```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. donkeylite.proto
```

Tutorial:
```
https://engineering.semantics3.com/a-simplified-guide-to-grpc-in-python-6c4e25f0c506
```