import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

from src.utils.OpenTelemetry.config import SERVICE_NAME


def check_health(host, port, service_name):
    try:
        with grpc.insecure_channel(f"{host}:{port}") as channel:
            stub = health_pb2_grpc.HealthStub(channel)
            request = health_pb2.HealthCheckRequest(service=service_name)
            response = stub.Check(request)
            if response.status == health_pb2.HealthCheckResponse.SERVING:
                print("SERVING")
                return 0  # Healthy
            else:
                print("NOT_SERVING")
                return 1  # Unhealthy
    except Exception as e:
        print(f"Health check failed: {e}")
        return 1  # Unhealthy


if __name__ == "__main__":
    import sys

    sys.exit(check_health(SERVICE_NAME, 50051, SERVICE_NAME))
