from pathlib import Path

import importlib_metadata
from vnpy.trader.app import BaseApp
from vnpy.trader.constant import Direction
from vnpy.trader.object import TickData, BarData, TradeData, OrderData
from vnpy.trader.utility import BarGenerator, ArrayManager

from .base import APP_NAME, StopOrder
from .engine import CtaEngine
from .template import CtaTemplate, Signal, TargetPosTemplate

try:
    __version__ = importlib_metadata.version("vnpy_ctastrategy")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"


class CtaStrategyApp(BaseApp):
    """"""

    app_name: str = APP_NAME
    app_module: str = __module__
    app_path: Path = Path(__file__).parent
    display_name: str = "CTA策略"
    engine_class: CtaEngine = CtaEngine
    widget_name: str = "CtaManager"
    icon_name: str = str(app_path.joinpath("ui", "cta.ico"))
