
all: client

client:
	go get
	protoc parser.proto --go_out=plugins=grpc:.
