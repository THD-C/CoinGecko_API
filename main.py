import grpc
from fastapi import FastAPI
import requests
import json
import time
from dotenv import load_dotenv
from os import getenv
import coins.coins_pb2
import coins.coins_pb2_grpc
from concurrent import futures
import time


load_dotenv()


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

async def coin_data(id: str):
    url = 'https://api.coingecko.com/api/v3/coins/' + id
    params = {
        'localization': 'false',
        'tickers': 'false',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    headers = {'x-cg-demo-api-key': getenv('COINGECKO_API_KEY')}

    response = requests.get(url, params=params)

    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"message": 'Failed to retrieve data from the API'}



async def cache_coins_id():
    url = 'https://api.coingecko.com/api/v3/coins/list'

    headers = {'x-cg-demo-api-key': getenv('COINGECKO_API_KEY')}

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print('works here')
        with open('cache.txt', 'w') as file:
            file.write(f"{int(time.time())}\n")
            json.dump(data, file)
            return 0
    else:
        return 1
