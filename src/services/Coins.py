from google.protobuf import struct_pb2

import coins.coins_pb2
import coins.coins_pb2_grpc
import asyncio

from currency import currency_pb2, currency_type_pb2
from src.connections import currency_stub
from concurrent.futures import ThreadPoolExecutor





class CoinsService(coins.coins_pb2_grpc.CoinsServicer):
    requester = None
    def __init__(self, requester):
        self.requester = requester
    def GetCoinData(self, request, context):
        print(f"Received coin data request for coin_id: {request.coin_id}")

        inputData = {
            "coin_id": request.coin_id,
            "fiat_currency": request.fiat_currency
        }

        requesterResponse = self.requester.getCoinData(inputData)

        if "error" in requesterResponse:
            response = coins.coins_pb2.DataResponse(
                status="error",
                error_message=requesterResponse['error'],
                data=""
            )
        else:
            formatted_data = {
                "id": requesterResponse['data']['id'],
                "symbol": requesterResponse['data']['symbol'],
                "name": requesterResponse['data']['name'],
                "market_data": {
                    "current_price": requesterResponse['data']['market_data']['current_price'][inputData["fiat_currency"]],
                    "market_cap": requesterResponse['data']['market_data']['market_cap'][inputData["fiat_currency"]],
                    "total_volume": requesterResponse['data']['market_data']['total_volume'][inputData["fiat_currency"]],
                    "high_24h": requesterResponse['data']['market_data']['high_24h'][inputData["fiat_currency"]],
                    "low_24h": requesterResponse['data']['market_data']['low_24h'][inputData["fiat_currency"]],
                    "price_change_24h_in_currency": requesterResponse['data']['market_data']['price_change_24h_in_currency'][inputData["fiat_currency"]],
                    "price_change_percentage_24h_in_currency": requesterResponse['data']['market_data']['price_change_percentage_24h_in_currency'][inputData["fiat_currency"]],
                }
            }

            response = coins.coins_pb2.DataResponse(
                status="success",
                error_message="",
                data=formatted_data
            )
        return response

    def GetHistoricalData(self, request, context):
        print(f"Received historical data request for coin_id: {request.coin_id}")

        inputData = {
            "coin_id": request.coin_id,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "fiat_currency": request.fiat_currency
        }

        requesterResponse = self.requester.getHistoricalChartData(inputData)

        if "error" in requesterResponse is not None:
            response = coins.coins_pb2.DataResponse(
                status="error",
                error_message=requesterResponse['error'],
                data=""
            )
        else:
            formatted_data = {
                "timestamp": [],
                "price": []
            }

            for timestamp, price in requesterResponse['data']['prices']:
                formatted_data["timestamp"].append(timestamp)
                formatted_data["price"].append(price)

            response = coins.coins_pb2.DataResponse(
                status="success",
                error_message="",
                data=formatted_data
            )
        return response

    def GetAllCoinsPrices(self, request, context):
        coin_prices = {}
        error_flag = 0

        fiat_currencies_list = currency_stub.GetSupportedCurrencies(currency_pb2.CurrencyTypeMsg(type=currency_type_pb2.CURRENCY_TYPE_FIAT))

        print("fiats: ", fiat_currencies_list)

        responses = self.requester.getAllCoinsData()

        for response in responses:
            if "error" in response:
                error_flag += 1
                continue
            coin_prices[response['data']['id']] = {}
            for fiat_coin in fiat_currencies_list.currencies:
                coin_prices[response['data']['id']][fiat_coin.currency_name] = response['data']['market_data']['current_price'][fiat_coin.currency_name]

        print("coin_prices: ", coin_prices)

        if error_flag != 0:
            response = coins.coins_pb2.DataResponse(
                status="error",
                error_message=f"Couldn't fetch data for {error_flag} currencies",
                data=""
            )
        else:
            formatted_data = coin_prices
            response = coins.coins_pb2.DataResponse(
                status="success",
                error_message="",
                data=formatted_data
            )
        return response

    def GetListDataForAllCoins(self, request, context):
        coinsList = {}
        error_flag = 0

        responses = self.requester.getAllCoinsData()

        for response in responses:
            if "error" in response:
                error_flag += 1
                continue
            coinsList[response['data']['id']] = response['data']

        if error_flag != 0:
            response = coins.coins_pb2.ListDataForAllCoinsResponse(
                status="error",
                error_message=f"Couldn't fetch data for {error_flag} currencies",
                data={}
            )
        else:
            formatted_data = {}
            for coin_id, coin_data in coinsList.items():
                formatted_data[coin_id] = {
                    "id": coin_data['id'],
                    "symbol": coin_data['symbol'],
                    "name": coin_data['name'],
                    "market_data": {
                        "current_price": coin_data['market_data']['current_price'][request.fiat_currency],
                        "market_cap": coin_data['market_data']['market_cap'][request.fiat_currency],
                        "total_volume": coin_data['market_data']['total_volume'][request.fiat_currency],
                        "high_24h": coin_data['market_data']['high_24h'][request.fiat_currency],
                        "low_24h": coin_data['market_data']['low_24h'][request.fiat_currency],
                        "price_change_24h_in_currency": coin_data['market_data']['price_change_24h_in_currency'][
                            request.fiat_currency],
                        "price_change_percentage_24h_in_currency":
                            coin_data['market_data']['price_change_percentage_24h_in_currency'][request.fiat_currency],
                    }
                }

            response = coins.coins_pb2.ListDataForAllCoinsResponse(
                status="success",
                error_message=""
            )

            for key, value in formatted_data.items():
                struct_item = struct_pb2.Struct()
                struct_item.update({key: value})
                response.data.append(struct_item)

        return response
