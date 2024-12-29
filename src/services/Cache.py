import time


class Cache:
    _instance = None

    GETCOINDATA_TTL = 60*2
    GETHISTORICALCHARTDATA_TTL = 60*60*24
    GETALLCOINPRICES_TTL = 60*5

    cache = {
        "getCoinData": {},
        "getHistoricalChartData": {},
        "getAllCoinsData": {}
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getFromCache(self, function, request=None):
        current_timestamp = int(time.time())
        if function == "getCoinData":
            try:
                if current_timestamp < self.GETCOINDATA_TTL+self.cache[function][request['coin_id']]['timestamp']:
                    return self.cache[function][request['coin_id']]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        elif function == "getHistoricalChartData":
            try:
                if current_timestamp < self.GETCOINDATA_TTL + self.cache[function][request['coin_id']]['timestamp']:
                    return self.cache[function][request['coin_id']]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        elif function == "getAllCoinsData":
            try:
                if current_timestamp < self.GETALLCOINPRICES_TTL + self.cache[function]['timestamp']:
                    return self.cache[function]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        else:
            return {"error": "Wrong request name given for getFromCache"}

    def addToCache(self, function, response, request=None):
        current_timestamp = int(time.time())

        if "error" in response is not None:
            return

        if function == "getCoinData":
            self.cache[function][request["coin_id"]] = {}
            self.cache[function][request["coin_id"]]['timestamp'] = current_timestamp
            self.cache[function][request["coin_id"]]['data'] = response
        elif function == "getHistoricalChartData":
            return
        elif function == "getAllCoinsData":
            self.cache[function] = {}
            self.cache[function]['timestamp'] = current_timestamp
            self.cache[function]['data'] = response
        else:
            return

    def removeFromCache(self, function, request):
        if function == "getCoinData":
            self.cache[function].pop(request["coin_id"])
        elif function == "getHistoricalChartData":
            return 1
        elif function == "getAllCoinsData":
            self.cache[function].pop('timestamp')
            self.cache[function].pop('data')
        else:
            return 0
