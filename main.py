import grpc
import coins.coins_pb2
import coins.coins_pb2_grpc
from concurrent import futures
from services.Coins import CoinsService


def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    coins.coins_pb2_grpc.add_CoinsServicer_to_server(CoinsService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051...")
    while True:
        continue


if __name__ == "__main__":
    serve()
