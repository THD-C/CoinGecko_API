import coins.coins_pb2
import coins.coins_pb2_grpc


class CoinsService(coins.coins_pb2_grpc.CoinsServicer):
    def GetCoinData(self, request, context):
        # Log the request for debugging
        print(f"Received request for coin_id: {request.coin_id}")

        # Create a response with the given coin_id and "0" for coin_data
        response = coins.coins_pb2.CoinData(
            coin_id=request.coin_id,
            coin_data="0"
        )
        return response
