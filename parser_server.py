import grpc
from concurrent import futures
import time
from parser_util import parseData
import parser_pb2
import parser_pb2_grpc

class LemillionParserServicer(parser_pb2_grpc.LemillionParserServicer):

    def parseData(self,request, context):
        response = parser_pb2.ParseReply()
        response.text = parseData(request.pages)
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

parser_pb2_grpc.add_LemillionParserServicer_to_server(LemillionParserServicer(),server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)