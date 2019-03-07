import grpc
from concurrent import futures
import time
from parser_util import parseData
import parser_pb2
import parser_pb2_grpc

class ParserServicer(parser_pb2_grpc.ParserServicer):

    def parse(self,request, context):
        response = parser_pb2.ParseReply()
        response.paragraphs[:] = parseData(request.pagesJSON)
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

parser_pb2_grpc.add_ParserServicer_to_server(ParserServicer(),server)

print('Starting server. Listening on port 50052.')
server.add_insecure_port('[::]:50052')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)