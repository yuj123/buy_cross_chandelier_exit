# Backtesting buy and hold strategy with price cross down Chandelier Exit

1. This is an example of backtesting with BackTrader.

2. It is a buy and hold strategy on the signal: Death cross down of chandelier line / price.

3. Normally, the death cross signals algorithmic traders to trigger the trailing stop loss of the equity.

4. From a different angle, "Greedy When Others Are Fearful", it is on sales, especially for high growth potential equity.

5. The program buys equity when the dealth cross appears under short-term oversold.

5. It uses (RSA < 35) as oversold signals, in order to minimize the number of trades per year.

6. It backtests the strategy with some Hong Kong Exchange Equity and sees the profit and loss.

7. Those equities are common in "Monthly Stocks Investment Plan", local bank offers.

## Result

```
> python buy_cross_chan_exit.py | grep pct
pct_chg(0027)=16.34%
pct_chg(0066)=12.68%
pct_chg(0762)=0.67%
pct_chg(1038)=23.40%
pct_chg(1928)=1.41%
pct_chg(2318)=9.76%
pct_chg(2388)=11.74%
```

## Reference:
https://www.backtrader.com/docu/quickstart/quickstart.html

http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chandelier_exit
