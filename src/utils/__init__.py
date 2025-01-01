import os

try:
    MONGO_MANAGER_PORT = os.getenv("MONGO_MANAGER_PORT", default="50052")
    MONGO_MANAGER = os.getenv("MONGO_MANAGER", default="localhost")
    GETCOINDATA_TTL = os.getenv("GETCOINDATA_TTL", default=60*2) # 2 minutes
    GETHISTORICALCHARTDATA_TTL = os.getenv("GETHISTORICALCHARTDATA_TTL", default=60*60*24) # 1 day
    GETHISTORICALCANDLECHARTDATA_TTL = os.getenv("GETHISTORICALCANDLECHARTDATA_TTL", default=60 * 60 * 24)  # 1 day
    GETALLCOINPRICES_TTL = os.getenv("GETALLCOINPRICES_TTL", default=60*5) # 5 minutes
    CACHE_TTL = os.getenv("CACHE_TTL", default=60*60*24) # 1 day
except Exception as e:
    print(f"Error occured when loading environment variables: {e}")