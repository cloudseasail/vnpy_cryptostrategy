# encoding: UTF-8

# from vnpy.trader import vtConstant
# from .ccxtGateway import CcxtGateway

# gatewayClass = CcxtGateway
# gatewayName = 'CCXT'
# gatewayDisplayName = 'CCXT'
# gatewayType = vtConstant.GATEWAYTYPE_BTC
# gatewayQryEnabled = True


from .constant import ExchangeExtend, IntervalExtend

def init() -> None:
    """Patch original VeighNa framework to support cryptocurrency"""
    import vnpy.trader.constant

    vnpy.trader.constant.Exchange = ExchangeExtend
    vnpy.trader.constant.Interval = IntervalExtend

def init_vnpy_crypto()-> None:
    init()

    try:
        vnpy_okex()
    except:
        print("skip hacking vnpy_okex")
    
    try:
        vnpy_binance()
    except:
        print("skip hacking vnpy_binance")


def vnpy_okex() -> None:
    from vnpy.trader.constant import Interval
    import vnpy_okex
    vnpy_okex.okex_gateway.INTERVAL_VT2OKEX = {
        Interval.MINUTE: "1m",
        Interval.HOUR: "1H",
        Interval.DAILY: "1D",
        Interval.MINUTE_15: "15m",
    }
def vnpy_binance() -> None:
    from vnpy.trader.constant import Interval
    import vnpy_binance
    vnpy_binance.binance_spot_gateway.INTERVAL_VT2BINANCE = {
        Interval.MINUTE: "1m",
        Interval.HOUR: "1h",
        Interval.DAILY: "1d",
        Interval.MINUTE_15: "15m",
    }
