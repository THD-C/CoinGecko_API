import time

from src.utils import GETCOINDATA_TTL, GETHISTORICALCHARTDATA_TTL, GETALLCOINPRICES_TTL, CACHE_TTL, GETHISTORICALCANDLECHARTDATA_TTL


class Cache:
    _instance = None

    cache = {
        "getCoinData": {},
        "getHistoricalChartData": {},
        "getHistoricalCandleChartData": {},
        "getAllCoinsData": {}
    }

    creationTime = int(time.time())

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def getFromCache(self, function, request=None):
        current_timestamp = int(time.time())
        self.cacheCheckAndCleanup(current_timestamp)
        if function == "getCoinData":
            try:
                if current_timestamp < GETCOINDATA_TTL+self.cache[function][request['coin_id']]['timestamp']:
                    return self.cache[function][request['coin_id']]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        elif function == "getHistoricalChartData":
            try:
                start_timestamp = request["start_date"].ToSeconds()
                end_timestamp = request["end_date"].ToSeconds()
                coin_id = request["coin_id"]
                fiat_currency = request["fiat_currency"]

                if current_timestamp < GETHISTORICALCHARTDATA_TTL + self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency]['timestamp']:
                    return self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        elif function == "getHistoricalCandleChartData":
            try:
                start_timestamp = request["start_date"].ToSeconds()
                end_timestamp = request["end_date"].ToSeconds()
                coin_id = request["coin_id"]
                fiat_currency = request["fiat_currency"]

                if current_timestamp < GETHISTORICALCANDLECHARTDATA_TTL + self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency]['timestamp']:
                    return self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency]['data']
                else:
                    self.removeFromCache(function, request)
                    return 0
            except KeyError:
                return 0
        elif function == "getAllCoinsData":
            try:
                if current_timestamp < GETALLCOINPRICES_TTL + self.cache[function]['timestamp']:
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

        if function == "getCoinData":
            if "error" in response is not None:
                return
            self.cache[function][request["coin_id"]] = {}
            self.cache[function][request["coin_id"]]['timestamp'] = current_timestamp
            self.cache[function][request["coin_id"]]['data'] = response
        elif function == "getHistoricalChartData" or function == "getHistoricalCandleChartData":
            if "error" in response is not None:
                return
            start_timestamp = request["start_date"].ToSeconds()
            end_timestamp = request["end_date"].ToSeconds()
            coin_id = request["coin_id"]
            fiat_currency = request["fiat_currency"]

            if coin_id not in self.cache[function]:
                self.cache[function][coin_id] = {}
            if start_timestamp not in self.cache[function][coin_id]:
                self.cache[function][coin_id][start_timestamp] = {}
            if end_timestamp not in self.cache[function][coin_id][start_timestamp]:
                self.cache[function][coin_id][start_timestamp][end_timestamp] = {}
            if fiat_currency not in self.cache[function][coin_id][start_timestamp][end_timestamp]:
                self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency] = {}

            self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency]['timestamp'] = current_timestamp
            self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency]['data'] = response
            return
        elif function == "getAllCoinsData":
            for responseeeeeXDDDD in response:
                if "error" in responseeeeeXDDDD:
                    return

            self.cache[function] = {}
            self.cache[function]['timestamp'] = current_timestamp
            self.cache[function]['data'] = response
        else:
            return

    def removeFromCache(self, function, request):
        if function == "getCoinData":
            self.cache[function].pop(request["coin_id"])
        elif function == "getHistoricalChartData" or function == "getHistoricalCandleChartData":
            start_timestamp = request["start_date"].ToSeconds()
            end_timestamp = request["end_date"].ToSeconds()
            coin_id = request["coin_id"]
            fiat_currency = request["fiat_currency"]

            self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency].pop('timestamp')
            self.cache[function][coin_id][start_timestamp][end_timestamp][fiat_currency].pop('data')
        elif function == "getAllCoinsData":
            self.cache[function].pop('timestamp')
            self.cache[function].pop('data')
        else:
            return 0

    def cacheCheckAndCleanup(self, current_timestamp):
        if current_timestamp > CACHE_TTL + self.creationTime:
            self.cache = {
                "getCoinData": {},
                "getHistoricalChartData": {},
                "getHistoricalCandleChartData": {},
                "getAllCoinsData": {}
            }
            self.creationTime = current_timestamp
