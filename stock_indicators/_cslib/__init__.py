"""
Skender.Stock.Indicators
~~~~~~~~~~~~~~~~~~~~~~~~

This module loads `Skender.Stock.Indicators.dll`(v1.23.1), which is a compiled library package
from <https://github.com/DaveSkender/Stock.Indicators>, written in C#.

It is currently using `.NET 6.0`.
"""

import os

try:
    from pythonnet import load
    load(runtime="coreclr",
        runtime_config=os.path.join(os.path.dirname(__file__), 'runtimeconfig.json'))

finally:
    try:
        import clr

    except:
        raise ImportError(("fail to import clr.\n"
        "Stock Indicators for Python has dependency on pythonnet, which uses CLR.\n"
        "Check that you have CLR installed, such as .NET6.0+ or Mono.\n"
        ".NET:\n\t"
        "https://dotnet.microsoft.com/en-us/download/dotnet\n"
        "Mono:\n\t"
        "https://www.mono-project.com/download/stable/"))

skender_stock_indicators_dll_path = os.path.join(
    os.path.dirname(__file__),
    "lib/Skender.Stock.Indicators.dll"
)
clr.AddReference(skender_stock_indicators_dll_path)
clr.AddReference('System.Collections')

# Built-in
from System import DateTime as CsDateTime
from System import Decimal as CsDecimal
from System import Enum as CsEnum
from System.Globalization import CultureInfo
from System.Collections.Generic import List as CsList

# Classes
from Skender.Stock.Indicators import CandleProperties as CsCandleProperties
from Skender.Stock.Indicators import Indicator as CsIndicator
from Skender.Stock.Indicators import Quote as CsQuote
from Skender.Stock.Indicators import ResultBase as CsResultBase

# Enums
from Skender.Stock.Indicators import BetaType as CsBetaType
from Skender.Stock.Indicators import CandlePart as CsCandlePart
from Skender.Stock.Indicators import ChandelierType as CsChandelierType
from Skender.Stock.Indicators import EndType as CsEndType
from Skender.Stock.Indicators import MaType as CsMaType
from Skender.Stock.Indicators import PeriodSize as CsPeriodSize
from Skender.Stock.Indicators import PivotPointType as CsPivotPointType
from Skender.Stock.Indicators import PivotTrend as CsPivotTrend
from Skender.Stock.Indicators import Match as CsMatch
