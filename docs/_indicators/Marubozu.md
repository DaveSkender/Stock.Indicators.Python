---
title: Marubozu (Preview)
permalink: /indicators/Marubozu/
layout: indicator
type: candlestick-pattern
---

# {{ page.title }}
<hr>

## **get_marubozu**(*quotes, min_body_percent=0.95*)

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable(such as list or an object having `__iter__()`) of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes).
| `min_body_percent` | float, *default 0.95* | Minimum body size as a decimalized percent of total candle size.  Must be between 0.8 and 1, if specified.

### Historical quotes requirements

You must have at least one historical quote; however, more is typically provided since this is a chartable candlestick pattern.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
CandleResults[CandleResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `CandleResults` is just a list of `CandleResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The candlestick pattern is indicated on dates where `signal` is `Signal.BULL_SIGNAL` or `Signal.BEAR_SIGNAL`.
- `price` is `close` price; however, all OHLC elements are included in the `candle` properties.
- There is no intrinsic basis or confirmation signal provided for this pattern.

{% include candle-result.md %}

### Utilities

- [.condense()]({{site.baseurl}}/utilities#condense)
- [.find(lookup_date)]({{site.baseurl}}/utilities#find-indicator-result-by-date)
- [.remove_warmup_periods(qty)]({{site.baseurl}}/utilities#remove-warmup-periods)

See [Utilities and Helpers]({{site.baseurl}}/utilities#utilities-for-indicator-results) for more information.

## Example

```python
from stock_indicators import indicators

# This method is NOT a part of the library.
quotes = get_history_from_feed("SPY")

# Calculate
results = indicators.get_marubozu(quotes);
```

## About: {{ page.title }}

[Marubozu](https://en.wikipedia.org/wiki/Marubozu) is a single candlestick pattern that has no wicks, representing consistent directional movement.
[[Discuss] :speech_balloon:]({{site.github.base_repository_url}}/discussions/512 "Community discussion about this indicator")

![image]({{site.charturl}}/Marubozu.png)

### Sources

- [C# core]({{site.base_sourceurl}}/m-r/Marubozu/Marubozu.cs)
- [Python wrapper]({{site.sourceurl}}/marubozu.py)