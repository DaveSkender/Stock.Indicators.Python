---
title: Ulcer Index (UI)
permalink: /indicators/UlcerIndex/
type: price-characteristic
layout: indicator
---

# {{ page.title }}
<hr>

## **get_ulcer_index**(*quotes, lookback_periods=14*)
    
## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable(such as list or an object having `__iter__()`) of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [Got in trouble with Pandas.dataframe?]({{site.baseurl}}/guide/#using-pandasdataframe) </span>
| `lookback_periods` | int, *default 14* | Number of periods (`N`) for review.  Must be greater than 0.

### Historical quotes requirements

You must have at least `N` periods of `quotes` to cover the warmup periods.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
UlcerIndexResults[UlcerIndexResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `UlcerIndexResults` is just a list of `UlcerIndexResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `N-1` periods will have `None` values since there's not enough data to calculate.

### UlcerIndexResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `ui` | float, Optional | Ulcer Index

### Utilities

- [.find(lookup_date)]({{site.baseurl}}/utilities#find-indicator-result-by-date)
- [.remove_warmup_periods()]({{site.baseurl}}/utilities#remove-warmup-periods)
- [.remove_warmup_periods(qty)]({{site.baseurl}}/utilities#remove-warmup-periods)

See [Utilities and Helpers]({{site.baseurl}}/utilities#utilities-for-indicator-results) for more information.

## Example

```python
from stock_indicators import indicators

# This method is NOT a part of the library.
quotes = get_history_from_feed("SPY")

# Calculate UI(14)
results = indicators.get_ulcer_index(quotes, 14)
```

# About: {{ page.title }}

Created by Peter Martin, the [Ulcer Index](https://en.wikipedia.org/wiki/Ulcer_index) is a measure of downside Close price volatility over a lookback window.
[[Discuss] :speech_balloon:]({{site.github.base_repository_url}}/discussions/232 "Community discussion about this indicator")

![image]({{site.charturl}}/UlcerIndex.png)

### Sources

- [C# core]({{site.base_sourceurl}}/s-z/UlcerIndex/UlcerIndex.cs)
- [Python wrapper]({{site.sourceurl}}/ulcer_index.py)
