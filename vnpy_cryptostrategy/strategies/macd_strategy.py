from vnpy_cryptostrategy import (
    CtaTemplate,
    StopOrder,
    Signal,
    BarGenerator,
    ArrayManager,
    TickData,
    BarData,
    TradeData,
    OrderData
)
from vnpy.trader.constant import Offset,Direction

from time import time

from vnpy_cryptostrategy.strategies.order_optimizer import OrderOptimizer

class MacdSignal(Signal):
    """"""

    def __init__(self, fast_period: int,
                 slow_period: int,
                 signal_period: int):
        """Constructor"""
        super().__init__()

        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

        self.strength = 3

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager(size=365)
        self.first = None

        self.macd_hist =[]

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.am.update_bar(bar)
        self.macd, self.signal, self.hist = self.am.macd(fast_period=self.fast_period,
                     slow_period=self.slow_period,
                     signal_period=self.signal_period,
                     array=True)
        return self.detect(self.hist)
        
    def detect(self, hist):
        signal = None
        h1 = hist[-1]
        h2 = hist[-2]
        # hist reverse 
        if self._reverse(h1, h2):
            self.macd_hist = []    #clear

        # moving out of window
        if len(self.macd_hist) > 0:
            if (self.am.count - self.macd_hist[0]['idx']) >= self.am.size:
                del self.macd_hist[0]
        if len(self.macd_hist) > 0:
            if self.check_inflection(h1,h2):
                self.macd_hist[-1]['inflection'] = True    # inflection found
                # print(self.macd_hist[-1])
                if len(self.macd_hist) >= self.strength:
                    if (self.check_trend() == True):
                        if self.check_divergence() == True:
                            signal = self.gen_signal()
                            print("signal %s, count %d, close %f" %(signal, self.am.count, self.am.close[-1]))
                    else:
                        del self.macd_hist[0]  # not trending, remove the oldest
            else:
                del self.macd_hist[-1]  # replace with new

        self.macd_hist.append({'idx':self.am.count, 'hist': h1, 'delta': h1-h2, 'inflection':False})
        return signal
    def check_inflection(self, h1, h2):
        if (self._reverse(self.macd_hist[-1]['delta'], h1-h2) == True) and (self._reverse(self.macd_hist[-1]['hist'], h1-h2)==True):
            return True
        else:
            return False
    def check_trend(self):
        # hist abs should get smaller
        for i in range(len(self.macd_hist)-1):
            if abs(self.macd_hist[i]['hist']) <= abs(self.macd_hist[i+1]['hist']):
                return False
        return True
    def check_divergence(self):
        for i in range(len(self.macd_hist)-1):
            id1 = self.macd_hist[i]['idx'] - self.am.count - 1
            id2 = self.macd_hist[i+1]['idx'] - self.am.count - 1
            if self.macd_hist[i]['hist']<0:
                if self.am.low[id1] < self.am.low[id2]:
                    return False
            else:
                if self.am.high[id1] > self.am.high[id2]:
                    return False
        return True
    def _reverse(self, h1, h2):
        if (h2<0 and h1>=0) or (h2>0 and h1<=0):
            return True
        else:
            return False
    def gen_signal(self):
        if self.macd_hist[-1]['hist']<0:
            return "LONG"
        else:
            return "SHORT"

class MacdStrategy(CtaTemplate):
    """"""
    author = "用Python的交易员"

    macd_fast_period = 12
    macd_slow_period = 26
    macd_signal_period = 9
    reward_risk_ratio = 1.5

    risk_percent_min = 0.004
    risk_percent_max = 0.1

    parameters = ["macd_fast_period", "macd_slow_period", "macd_signal_period"]
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.macd_signal = MacdSignal(self.macd_fast_period, self.macd_slow_period, self.macd_signal_period)
        self.order_optimizer = OrderOptimizer()

    @property
    def am(self):
        return self.macd_signal.am

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(self.macd_slow_period+self.macd_signal_period)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")
        self.put_event()

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.macd_signal.on_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        signal = self.macd_signal.on_bar(bar)
        self.hanlde_signal(signal)


        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        self.put_event()

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        if trade.offset == Offset.OPEN:
            self.on_trade_open(trade)
        if trade.offset == Offset.CLOSE:
            self.on_trade_close(trade)
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        self.put_event()

    def hanlde_signal(self, signal):
        if signal == 'LONG':
            if self.pos == 0:
                self.cancel_all()
                price = self.am.close[-1]
                vol = self.order_optimizer.opt_position(price, self.cta_engine.capital)
                self.buy(price=price, volume=vol)
                
        if signal == 'SHORT':
            if self.pos == 0:
                self.cancel_all()
                price = self.am.close[-1]
                vol = self.order_optimizer.opt_position(price, self.cta_engine.capital)
                self.short(price=price, volume=vol)
            
    def on_trade_open(self, trade: TradeData):
        atr = self.am.atr(n=3)
        atr = self.order_optimizer.opt_stop_atr(trade.price, atr, rp_min=self.risk_percent_min, rp_max=self.risk_percent_max)
        
        if trade.direction == Direction.LONG:
            self.sell(price=trade.price + (self.reward_risk_ratio*atr), volume=trade.volume)
            self.sell(price=trade.price - atr, volume=trade.volume, stop=True)
        
        if trade.direction == Direction.SHORT:
            self.cover(price=trade.price- (self.reward_risk_ratio*atr), volume=trade.volume)
            self.cover(price=trade.price + atr, volume=trade.volume, stop=True)

    def on_trade_close(self, trade: TradeData):
        self.cancel_all()

