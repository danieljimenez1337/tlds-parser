import grpc
import json
# import the generated classes
import parser_pb2
import parser_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50052')

# create a stub (client)
stub = parser_pb2_grpc.ParserStub(channel)

#get json
data =[]
with open('testdata/data.json') as json_data:
    j = json.load(json_data)["pages"]
    for x in j:
        data.append(json.dumps(x))



# create a valid request message
array = parser_pb2.ParseRequest(pagesJSON = data)
# make the call
response = stub.parse(array)

# et voilà
print(response.paragraphs)