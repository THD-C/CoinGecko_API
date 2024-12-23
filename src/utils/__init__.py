import os

try:
    MONGO_MANAGER_PORT = os.getenv("MONGO_MANAGER_PORT", default="50051")
    MONGO_MANAGER = os.getenv("MONGO_MANAGER", default="Mongo_Manager")
except Exception as e:
    print(f"Error occured when loading environment variables: {e}")