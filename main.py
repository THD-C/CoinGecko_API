from fastapi import FastAPI
import requests
from dotenv import load_dotenv
from os import getenv
load_dotenv()
app = FastAPI()


@app.get("/")
async def root():

    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'ethereum',
        'vs_currencies': 'USD'
    }

    headers = {'x-cg-demo-api-key': getenv('COINGECKO_API_KEY')}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        ethereum_price = data['ethereum']['usd']
        return {"message": f'The price of Ethereum in USD is ${ethereum_price}'}
    else:
        return {"message": 'Failed to retrieve data from the API'}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
