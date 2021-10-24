from typing import Iterable, Optional, Type
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

# TODO: Need to support CandlePart Enum
def get_ema(quotes: Iterable[Quote], lookback_periods: int):
    ema_list = CsIndicator.GetEma[Quote](CsList(Quote, quotes), lookback_periods)
    return EMAResults(ema_list, EMAResult)

class EMAResult(ResultBase):
    """
    A wrapper class for a single unit of EMA results.
    """

    def __init__(self, ema_result):
        super().__init__(ema_result)

    @property
    def ema(self):
        return to_pydecimal(self._csdata.Ema)

    @ema.setter
    def ema(self, value):
        self._csdata.Ema = CsDecimal(value)


class EMAResults(IndicatorResults[EMAResult]):
    """
    A wrapper class for the list of EMA(Exponential Moving Average) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in CSharp implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[EMAResult]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)
        
        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
