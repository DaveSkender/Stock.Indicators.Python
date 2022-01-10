from decimal import Decimal
from typing import Iterable, Optional, TypeVar
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_slope(quotes: Iterable[Quote], lookback_periods: int):
    results = CsIndicator.GetSlope[Quote](CsList(Quote, quotes), lookback_periods)
    return SlopeResults(results, SlopeResult)

class SlopeResult(ResultBase):
    """
    A wrapper class for a single unit of Slope results.
    """

    @property
    def slope(self) -> Optional[float]:
        return self._csdata.Slope

    @slope.setter
    def slope(self, value):
        self._csdata.Slope = value
        
    @property
    def intercept(self) -> Optional[float]:
        return self._csdata.Intercept
    
    @intercept.setter
    def intercept(self, value):
        self._csdata.Intercept = value
        
    @property
    def stdev(self) -> Optional[float]:
        return self._csdata.StdDev
    
    @stdev.setter
    def stdev(self, value):
        self._csdata.StdDev = value
        
    @property
    def r_squared(self) -> Optional[float]:
        return self._csdata.RSquared
    
    @r_squared.setter
    def r_squared(self, value):
        self._csdata.RSquared = value
    
    @property
    def line(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.Line)
    
    @line.setter
    def line(self, value):
        self._csdata.Line = CsDecimal(value)

T = TypeVar("T", bound=SlopeResult)
class SlopeResults(IndicatorResults[T]):
    """
    A wrapper class for the list of Slope results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)

        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        