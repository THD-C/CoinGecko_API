# CoinGecko API
Pobiera, udostępnia na zewnątrz poprzez gRPC, cachuje oraz zarządza danymi z CoinGecko.

# 1. Opis funkcji
## 1.1 GetHistoricalData():

### Parametry wejściowe:

```coin_id``` - id crypto coina z MongoDB

```start_date``` - data startowa jako timestamp

```end_date``` - data końcowa jako timestamp

### Paramtery wyjściowe:

```status``` - status operacji, success lub error

```error_message``` - jeśli status=error to opis błędu w przeciwnym wypadku puste

```data``` - jeśli status=success to słownik w przeciwnym wypadku puste
    
### Słownik data z przykładowego response:

Pierwszy rekord z tabeli timestamp odpowiada pierwszemu rekordowi z tabeli price.

    {
        timestamp: [
            1732230268459,
            1732234490890,
            1732238016359
        ],
        price: [
            98441.26161000447,
            98529.80211326091,
            98187.91803696626
        ]
    }

## 1.2 GetCoinData

### Parametry wejściowe:

```coin_id``` - id crypto coina z MongoDB
### Paramtery wyjściowe:

```status``` - status operacji, success lub error

```error_message``` - jeśli status=error to opis błędu w przeciwnym wypadku puste

```data``` - jeśli status=success to słownik w przeciwnym wypadku puste
    
### Słownik data z przykładowego response:

jako MONGO_FIAT można podstawić dowolną fiatową walutę z MongoDB, np. usd, pln, jpy, etc.

    {
       "id":"bitcoin",
       "symbol":"btc",
       "name":"Bitcoin",
       "market_data":{
          "current_price":{
             "MONGO_FIAT":351080
          },
          "market_cap":{
             "MONGO_FIAT":6948517954631
          },
          "total_volume":{
             "MONGO_FIAT":175359671780
          },
          "high_24h":{
             "MONGO_FIAT":366881
          },
          "low_24h":{
             "MONGO_FIAT":349429
          },
          "price_change_24h_in_currency":{
             "MONGO_FIAT":-12089.517051851959
          },
          "price_change_percentage_24h_in_currency":{
             "MONGO_FIAT":-3.32889
          }
       }
    }