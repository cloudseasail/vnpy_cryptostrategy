from enum import Enum

from vnpy.trader.constant import Exchange, Interval

class Exchange_(Enum):
    BINANCE = "BINANCE"
    HUOBI = "HUOBI"
    OKEX = "OKEX"
    COINBASE = "CONIBASE"
    BITFINEX = "BITFINEX"
 
ExchangeExtend = Enum(
    "Exchange",
    [(e.name, e.value) for e in Exchange] + [(e.name, e.value) for e in Exchange_] 
)



class Interval_(Enum):
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_4 = "2h"
    HOUR_6 = "6h"   
 
IntervalExtend = Enum(
    "Interval",
    [(e.name, e.value) for e in Interval] + [(e.name, e.value) for e in Interval_] ,
)