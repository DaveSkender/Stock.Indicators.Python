import pytest
from stock_indicators import indicators

class TestParabolicSAR:
    def test_standard(self, quotes):
        results = indicators.get_parabolic_sar(quotes)
        
        assert 502 == len(results)
        assert 488 == len(list(filter(lambda x: x.sar is not None, results)))
        
        r = results[14]
        assert 212.8300 == round(float(r.sar), 4)
        assert True == r.is_reversal
        
        r = results[16]
        assert 212.9924 == round(float(r.sar), 4)
        assert False == r.is_reversal
        
        r = results[94]
        assert 228.3600 == round(float(r.sar), 4)
        assert False == r.is_reversal
        
        r = results[501]
        assert 229.7662 == round(float(r.sar), 4)
        assert False == r.is_reversal
        
    def test_bad_data(self, bad_quotes):
        r = indicators.get_parabolic_sar(bad_quotes)
        assert 502 == len(r)
        
    def test_removed(self, quotes):
        results = indicators.get_parabolic_sar(quotes, 0.02, 0.2).remove_warmup_periods()
        
        assert 488 == len(results)
        
        last = results.pop()
        assert 229.7662 == round(float(last.sar), 4)
        assert False == last.is_reversal
        
    def test_exceptions(self, quotes):
        from System import ArgumentOutOfRangeException
        with pytest.raises(ArgumentOutOfRangeException):
            indicators.get_parabolic_sar(quotes, 0, 1)

        with pytest.raises(ArgumentOutOfRangeException):
            indicators.get_parabolic_sar(quotes, 6, 2)

        from Skender.Stock.Indicators import BadQuotesException
        with pytest.raises(BadQuotesException):
            indicators.get_parabolic_sar(quotes[:1], 0.02, 0.2)
            