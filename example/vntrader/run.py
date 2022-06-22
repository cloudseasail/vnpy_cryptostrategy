import vnpy_crypto
vnpy_crypto.init()

from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_binance import (
    BinanceSpotGateway,
    BinanceUsdtGateway,
    BinanceInverseGateway
)
from vnpy_ctp import CtpGateway
from vnpy_okex import OkexGateway
from vnpy_binance.binance_spot_gateway import BinanceSpotGateway

from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp
from vnpy_spreadtrading import SpreadTradingApp
from vnpy_algotrading import AlgoTradingApp
from vnpy_scripttrader import ScriptTraderApp
from vnpy_chartwizard import ChartWizardApp
from vnpy_rpcservice import RpcServiceApp
from vnpy_excelrtd import ExcelRtdApp
from vnpy_datamanager import DataManagerApp
from vnpy_datarecorder import DataRecorderApp
from vnpy_riskmanager import RiskManagerApp
from vnpy_webtrader import WebTraderApp


def main():
    """主入口函数"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    # main_engine.add_gateway(CtpGateway)
    # main_engine.add_gateway(BinanceSpotGateway)
    # main_engine.add_gateway(BinanceUsdtGateway)
    # main_engine.add_gateway(BinanceInverseGateway)

    main_engine.add_gateway(OkexGateway, "OKEX")
    main_engine.add_gateway(BinanceSpotGateway, "BinanceSpot")

    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(SpreadTradingApp)
    main_engine.add_app(AlgoTradingApp)

    main_engine.add_app(ScriptTraderApp)
    main_engine.add_app(ChartWizardApp)
    main_engine.add_app(RpcServiceApp)
    main_engine.add_app(ExcelRtdApp)
    main_engine.add_app(DataManagerApp)
    main_engine.add_app(DataRecorderApp)
    main_engine.add_app(RiskManagerApp)
    main_engine.add_app(WebTraderApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
