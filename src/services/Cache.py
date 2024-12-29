import time


class Cache:
    _instance = None

    GETCOINDATA_TTL = 20
    GETHISTORICALCHARTDATA_TTL = 60*60*24
    GETALLCOINPRICES_TTL = 60*5

    cache = {
        "getCoinData": {},
        "getHistoricalChartData": {},
        "getAllCoinPrices": {}
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getFromCache(self, function, request):
        current_timestamp = int(time.time())
        if function == "getCoinData":
            try:
                if current_timestamp < self.GETCOINDATA_TTL+self.cache['getCoinData'][request['coin_id']]['timestamp']:
                    return self.cache['getCoinData'][request['coin_id']]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        elif function == "getHistoricalChartData":
            if self.cache['getHistoricalChartData'][request.coin_id]['timestamp'] < current_timestamp + self.GETCOINDATA_TTL:
                return self.cache['getCoinData'][request.coin_id]['data']
            else:
                self.removeFromCache(function, request)
            return 0
        elif function == "getAllCoinPrices":
            if self.cache['getAllCoinPrices'][request.coin_id]['timestamp'] < current_timestamp + self.GETCOINDATA_TTL:
                return self.cache['getCoinData'][request.coin_id]['data']
            else:
                self.removeFromCache(function, request)
            return 0
        else:
            return {"error": "Wrong request name given for getFromCache"}

    def addToCache(self, function, request, response):
        current_timestamp = int(time.time())

        if "error" in response is not None:
            return

        if function == "getCoinData":
            self.cache['getCoinData'][request["coin_id"]] = {}
            self.cache['getCoinData'][request["coin_id"]]['timestamp'] = current_timestamp
            self.cache['getCoinData'][request["coin_id"]]['data'] = response
        elif function == "getHistoricalChartData":
            return
        elif function == "getAllCoinPrices":
            return
        else:
            return

    def removeFromCache(self, function, request):
        if function == "getCoinData":
            self.cache['getCoinData'].pop(request["coin_id"])
        elif function == "getHistoricalChartData":
            return 1
        elif function == "getAllCoinPrices":
            return 1
        else:
            return 0

