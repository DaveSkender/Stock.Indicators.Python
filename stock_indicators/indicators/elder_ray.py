from typing import Iterable, Optional, TypeVar

from stock_indicators._cslib import CsIndicator
from stock_indicators.indicators.common.helpers import RemoveWarmupMixin
from stock_indicators.indicators.common.indicator import Indicator, calculate_indicator
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote


class ElderRayResult(ResultBase):
    """
    A wrapper class for a single unit of Elder-ray Index results.
    """

    @property
    def ema(self) -> Optional[float]:
        return self._csdata.Ema

    @ema.setter
    def ema(self, value):
        self._csdata.Ema = value

    @property
    def bull_power(self) -> Optional[float]:
        return self._csdata.BullPower

    @bull_power.setter
    def bull_power(self, value):
        self._csdata.BullPower = value

    @property
    def bear_power(self) -> Optional[float]:
        return self._csdata.BearPower

    @bear_power.setter
    def bear_power(self, value):
        self._csdata.BearPower = value


_T = TypeVar("_T", bound=ElderRayResult)
class ElderRayResults(RemoveWarmupMixin, IndicatorResults[_T]):
    """
    A wrapper class for the list of Elder-ray Index results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """


class ElderRay(Indicator):
    is_chainee = False
    is_chainor = True

    indicator_method = CsIndicator.GetElderRay[Quote]
    chaining_method = None

    list_wrap_class = ElderRayResults
    unit_wrap_class = ElderRayResult


@calculate_indicator(indicator=ElderRay())
def get_elder_ray(quotes: Iterable[Quote], lookback_periods: int = 13) -> ElderRayResults[ElderRayResult]:
    """Get Elder-ray Index calculated.

    The Elder-ray Index depicts buying and selling pressure, also known as Bull and Bear Power.

    Parameters:
        `quotes` : Iterable[Quote]
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
    return (quotes, lookback_periods)
