from decimal import Decimal
from typing import Iterable, Optional, Type, TypeVar
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_elder_ray(quotes: Iterable[Quote], lookback_periods: int = 13):
    """Get Elder-ray Index calculated.
    
    The Elder-ray Index depicts buying and selling pressure, also known as Bull and Bear Power.
    
    Parameters:
        `quotes` : Iterable[Quotes]
            Historical price quotes.
        
        `lookback_periods` : int, defaults 13
            Number of periods for the EMA.
    
    Returns:
        `ElderRayResults[ElderRayResult]`
            ElderRayResults is list of ElderRayResult with providing useful helper methods.
    
    See more:
         - [Elder-ray Index Reference](https://daveskender.github.io/Stock.Indicators.Python/indicators/ElderRay/#content)
         - [Helper Methods](https://daveskender.github.io/Stock.Indicators.Python/utilities/#content)
    """
    results = CsIndicator.GetElderRay[Quote](CsList(Quote, quotes), lookback_periods)
    return ElderRayResults(results, ElderRayResult)

class ElderRayResult(ResultBase):
    """
    A wrapper class for a single unit of Elder-ray Index results.
    """

    @property
    def ema(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.Ema)

    @ema.setter
    def ema(self, value):
        self._csdata.Ema = CsDecimal(value)
        
    @property
    def bull_power(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.BullPower)
    
    @bull_power.setter
    def bull_power(self, value):
        self._csdata.BullPower = CsDecimal(value)
        
    @property
    def bear_power(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.BearPower)
    
    @bear_power.setter
    def bear_power(self, value):
        self._csdata.BearPower = CsDecimal(value)

T = TypeVar("T", bound=ElderRayResult)
class ElderRayResults(IndicatorResults[T]):
    """
    A wrapper class for the list of Elder-ray Index results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    def __init__(self, data: Iterable, wrapper_class: Type[T]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)

        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        