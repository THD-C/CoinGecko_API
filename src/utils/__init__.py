import os

try:
    MONGO_MANAGER_PORT = os.getenv("MONGO_MANAGER_PORT", default="50052")
    MONGO_MANAGER = os.getenv("MONGO_MANAGER", default="localhost")
except Exception as e:
    print(f"Error occured when loading environment variables: {e}")