from datetime import datetime as PyDateTime
from typing import Iterable, List, Type, TypeVar
from stock_indicators._cslib import CsIndicator, CsResultBase
from stock_indicators._cstypes import DateTime as CsDateTime
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import to_pydatetime

class ResultBase:
    """
    A base wrapper class for a single unit of the results.
    """
    def __init__(self, base_result: Type[CsResultBase]):
        super().__init__()
        self._csdata = base_result

    @property
    def date(self):
        return to_pydatetime(self._csdata.Date)
    
    @date.setter
    def date(self, value):
        self._csdata.Date = CsDateTime(value)

T = TypeVar("T", bound=ResultBase)
class IndicatorResults(List[T]):
    """
    A base wrapper class for the list of results.
    It provides helper methods written in CSharp implementation.
    """
    def __init__(self, data: Iterable, wrapper_class: Type[T]):
        super().__init__([ wrapper_class(i) for i in data ])
        self._csdata = data
        self._wrapper_class = wrapper_class

    def reload(self):
        """
        Reload a C# array of the results to perform more operations.
        It is usually called after `done()`
        """
        if self._csdata is None:
            self._csdata = [ i._csdata for i in self ]
        return self

    def done(self):
        """
        Remove a C# array of the results after finishing all operations.
        It is not necessary but saves memory.
        """
        self._csdata = None
        return self

    def _verify_data(func):
        """
        Check whether `_csdata` can be passed to helper method.    
        """
        def verify_data(self, *args):
            if not isinstance(self._csdata, list) or len(self._csdata) < 1:
                raise ValueError(f"Cannot {func.__name__}() an empty result.")

            if not isinstance(self._csdata[0], CsResultBase):
                raise TypeError(
                    "The data should be an instance of Skender.Stock.Indicators.ResultBase or its subclasses."
                )

            return func(self, *args)

        return verify_data

    @_verify_data
    def __add__(self, other: Type["IndicatorResults"]):
        return self.__class__(self._csdata.__add__(other._csdata), self._wrapper_class)

    @_verify_data
    def __mul__(self, other: Type["IndicatorResults"]):
        return self.__class__(self._csdata.__mul__(other._csdata), self._wrapper_class)

    @_verify_data
    def find(self, lookup_date: PyDateTime) -> Type[T]:
        if not isinstance(lookup_date, PyDateTime):
            raise TypeError(
                "lookup_date must be an instance of datetime.datetime."
            )

        result = CsIndicator.Find(CsList(type(self._csdata[0]), self._csdata), CsDateTime(lookup_date))
        return self._wrapper_class(result)

    @_verify_data
    def remove_warmup_periods(self, remove_periods: int):
        if not isinstance(remove_periods, int):
            raise TypeError(
                "remove_periods must be an integer."
            )

        removed_results = CsIndicator.RemoveWarmupPeriods[CsResultBase](CsList(type(self._csdata[0]), self._csdata), remove_periods)
        return self.__class__(removed_results, self._wrapper_class)
