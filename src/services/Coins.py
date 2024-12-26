import coins.coins_pb2
import coins.coins_pb2_grpc
from src.services.CoinGeckoRequester import CoinGeckoRequester

requester = CoinGeckoRequester()


class CoinsService(coins.coins_pb2_grpc.CoinsServicer):
    def GetCoinData(self, request, context):
        print(f"Received coin data request for coin_id: {request.coin_id}")

        inputData = {
            "coin_id": request.coin_id
        }

        requesterResponse = requester.getCoinData(inputData)

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
                    "current_price": requesterResponse['data']['market_data']['current_price'],
                    "market_cap": requesterResponse['data']['market_data']['market_cap'],
                    "total_volume": requesterResponse['data']['market_data']['total_volume'],
                    "high_24h": requesterResponse['data']['market_data']['high_24h'],
                    "low_24h": requesterResponse['data']['market_data']['low_24h'],
                    "price_change_24h_in_currency": requesterResponse['data']['market_data']['price_change_24h_in_currency'],
                    "price_change_percentage_24h_in_currency": requesterResponse['data']['market_data']['price_change_percentage_24h_in_currency'],
                }
            }

            print(formatted_data)
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
            "end_date": request.end_date
        }

        requesterResponse = requester.getHistoricalChartData(inputData)

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
