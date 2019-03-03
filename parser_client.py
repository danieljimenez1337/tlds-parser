import grpc

# import the generated classes
import parser_pb2
import parser_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50052')

# create a stub (client)
stub = parser_pb2_grpc.LemillionParserStub(channel)

#get json
f = open("testdata/data.json","r")
string = f.read()

# create a valid request message
string = parser_pb2.ParseRequest(pages = string)
# make the call
response = stub.parseData(string)

# et voilà
print(response.text)