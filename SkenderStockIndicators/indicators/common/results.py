from datetime import datetime as PyDateTime
from typing import Type
from Skender.Stock.Indicators import Indicator as CsIndicator
from Skender.Stock.Indicators import ResultBase as CsResultBase
from SkenderStockIndicators._cstypes import DateTime as CsDateTime
from SkenderStockIndicators._cstypes import List as CsList
from SkenderStockIndicators._cstypes import to_pydatetime


class ResultBase:
    """
    A base wrapper class for a single unit of the results.
    """

    def __init__(self, base_result):
        super().__init__()
        self.Date = to_pydatetime(base_result.Date)


class IndicatorResults(list):
    """
    A base wrapper class for the list of results. It provides helper methods written in CSharp implementation.
    """

    def __init__(self, data, wrapper_class: Type[ResultBase]):
        super().__init__([ wrapper_class(i) for i in data ])
        self._csdata = data
        self._wrapper_class = wrapper_class


    def _verify_data(func):
        """
        Check whether _csdata can be passed to helper method.    
        """
        def verify_data(self, *args):
            if not isinstance(self._csdata, list) or len(self._csdata) < 1:
                raise ValueError("Can't remove from empty result.")

            if not isinstance(self._csdata[0], CsResultBase):
                raise TypeError(
                    "The data should be an instance of Skender.Stock.Indicators.ResultBase or its subclasses."
                )

            return func(self, *args)

        return verify_data

    
    @_verify_data
    def find(self, lookup_date: PyDateTime) -> Type[ResultBase]:
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


    @_verify_data
    def remove_periods(self, remove_periods: int):
        if not isinstance(remove_periods, int):
            raise TypeError(
                "remove_periods must be an integer."
            )

        removed_results = CsIndicator.Remove[CsResultBase](CsList(type(self._csdata[0]), self._csdata), remove_periods)
        return self.__class__(removed_results, self._wrapper_class)

    