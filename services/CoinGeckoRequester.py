import json
from os import getenv
import time
import requests


class Cacher:
    def __init__(self):
        url = 'https://api.coingecko.com/api/v3/coins/list'

        headers = {'x-cg-demo-api-key': getenv('COINGECKO_API_KEY')}

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print('works here')
            with open('cache.txt', 'w') as file:
                file.write(f"{int(time.time())}\n")
                json.dump(data, file)