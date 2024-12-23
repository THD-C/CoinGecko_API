import grpc
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from prometheus_client import start_http_server
from py_grpc_prometheus.prometheus_client_interceptor import PromClientInterceptor
import src.utils.OpenTelemetry.OpenTelemetry as oTEL

from src.utils import MONGO_MANAGER_PORT, MONGO_MANAGER
from secret import secret_pb2_grpc


GrpcInstrumentorClient().instrument()
prometheus_interceptor = PromClientInterceptor()
start_http_server(8111)

try:

    mongo_manager_channel = grpc.insecure_channel(f'{MONGO_MANAGER}:{MONGO_MANAGER_PORT}')
    mongo_manager_channel = grpc.intercept_channel(mongo_manager_channel, prometheus_interceptor)
    
    secret_stub = secret_pb2_grpc.SecretStoreStub(mongo_manager_channel)
except grpc.RpcError as e:
    print(f"Error occurred when connecting to services: {e}")
