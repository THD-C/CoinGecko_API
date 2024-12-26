import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from dotenv import load_dotenv

from secret.secret_pb2 import SecretName
from src.connections import secret_stub

load_dotenv()

RequestsInstrumentor().instrument()

class CoinGeckoRequester:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CoinGeckoRequester, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    url = "https://api.coingecko.com/api/v3/coins/"

    headers = {
        "x-cg-demo-api-key": secret_stub.GetSecret(SecretName(name="COIN_GECKO_KEY")).value
    }

    def getCoinData(self, inputData):
        coin_id = inputData["coin_id"]

        url = f"{self.url}/{coin_id}"

        params = {
            "id": coin_id,
            "localization": "false",
            "tickers": "false",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false",
        }

        return self.request(url, params)

    def getHistoricalChartData(self, inputData):
        start_timestamp = inputData["start_date"].ToSeconds()
        end_timestamp = inputData["end_date"].ToSeconds()
        coin_id = inputData["coin_id"]
        fiat_currency = inputData["fiat_currency"]

        url = f"{self.url}/{coin_id}/market_chart/range"

        params = {
            "vs_currency": fiat_currency,
            "from": start_timestamp,
            "to": end_timestamp
        }

        return self.request(url, params)

    def getAllCoinPrices(self):
        coin_id = {
            "coin_id": "btc"
        }
        self.getCoinData(coin_id)

    def request(self, url, params):
        try:
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code == 200:
                return {"data": response.json()}
            else:
                return {
                    "error": f"Failed to fetch data: {response.status_code} = {response.text}"
                }
        except Exception as e:
            return {"error": str(e)}
