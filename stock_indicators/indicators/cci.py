from typing import Iterable, Optional, TypeVar

from stock_indicators._cslib import CsIndicator
from stock_indicators.indicators.common.helpers import RemoveWarmupMixin
from stock_indicators.indicators.common.indicator import Indicator, calculate_indicator
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote


class CCIResult(ResultBase):
    """
    A wrapper class for a single unit of Commodity Channel Index (CCI) results.
    """

    @property
    def cci(self) -> Optional[float]:
        return self._csdata.Cci

    @cci.setter
    def cci(self, value):
        self._csdata.Cci = value


_T = TypeVar("_T", bound=CCIResult)
class CCIResults(RemoveWarmupMixin, IndicatorResults[_T]):
    """
    A wrapper class for the list of Commodity Channel Index (CCI) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in CSharp implementation.
    """


class CCI(Indicator):
    is_chainee = False
    is_chainor = True

    indicator_method = CsIndicator.GetCci[Quote]
    chaining_method = None

    list_wrap_class = CCIResults
    unit_wrap_class = CCIResult


@calculate_indicator(indicator=CCI())
def get_cci(quotes: Iterable[Quote], lookback_periods: int = 20) -> CCIResults[CCIResult]:
    """Get CCI calculated.

    Commodity Channel Index (CCI) is an oscillator depicting deviation
    from typical price range, often used to identify cyclical trends.

    Parameters:
        `quotes` : Iterable[Quote]
            Historical price quotes.

        `lookback_periods` : int, defaults 20
            Number of periods in the lookback window.

    Returns:
        `CCIResults[CCIResult]`
            CCIResults is list of CCIResult with providing useful helper methods.

    See more:
         - [CCI Reference](https://daveskender.github.io/Stock.Indicators.Python/indicators/Cci/#content)
         - [Helper Methods](https://daveskender.github.io/Stock.Indicators.Python/utilities/#content)
    """
    return (quotes, lookback_periods)
