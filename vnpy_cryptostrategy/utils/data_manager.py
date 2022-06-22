from datetime import datetime

from vnpy.trader.engine import BaseEngine, MainEngine, EventEngine
from vnpy.trader.constant import Interval, Exchange
from vnpy_datamanager.engine import ManagerEngine

from vnpy.trader.utility import load_json
from threading import Thread


class DataManager(ManagerEngine):
    def __init__(self, main_engine=None,  event_engin=None):
        if main_engine is None:
            event_engine = EventEngine()
            main_engine = MainEngine(event_engine)

        super().__init__(main_engine, event_engine)
        self.main_engine.event_engine.register("eLog", lambda e: print(e.data))

    def connect(self, gateway_name: str, setting, gateway_class=None) -> None:
        gateway = self.main_engine.gateways.get(gateway_name, None)
        if not gateway:
            self.main_engine.add_gateway(gateway_class, gateway_name)

        if type(setting) is str:
            setting = load_json(setting)
            # setting['代理地址'] = '127.0.0.1'
            # setting['代理端口'] = '20171'

        self.main_engine.connect(setting, gateway_name)

    def download_bar_data(
            self,
            symbol: str,
            exchange: Exchange,
            interval: str,
            start: datetime,
        ) -> bool:

            self.thread = Thread(
                target=super().download_bar_data,
                args=(
                    symbol,
                    exchange,
                    interval,
                    start,
                )
            )
            self.thread.start()
            return True