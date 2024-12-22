import coins.coins_pb2
import coins.coins_pb2_grpc
from services.CoinGeckoRequester import CoinGeckoRequester

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
            print(requesterResponse['data'])
            response = coins.coins_pb2.DataResponse(
                status="success",
                error_message="",
                data=requesterResponse['data']
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
            print(requesterResponse['data'])
            response = coins.coins_pb2.DataResponse(
                status="success",
                error_message="",
                data=requesterResponse['data']
            )
        return response
