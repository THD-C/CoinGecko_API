import grpc
import coins.coins_pb2 as coins_pb2
import coins.coins_pb2_grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from src.services.Coins import CoinsService

from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from py_grpc_prometheus.prometheus_server_interceptor import PromServerInterceptor
from prometheus_client import start_http_server

def serve():
    GrpcInstrumentorServer().instrument()
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[PromServerInterceptor(enable_handling_time_histogram=True)],
    )
    coins.coins_pb2_grpc.add_CoinsServicer_to_server(CoinsService(), server)

    # Enable reflection
    SERVICE_NAMES = (
        coins_pb2.DESCRIPTOR.services_by_name["Coins"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    start_http_server(8111)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
