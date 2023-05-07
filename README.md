# Trade-Forex-Back-Test
A robot built to trade the gold market. Algorithm backtest for trading in the XAUUSD market.

# Concept
the `back_test_algoritm_one.py`:
Buying is done when RSI drops below 25 and MA is 200 below the closing price.
Selling is done when RSI drops below 75 and MA 200 is higher than the closing price.

the `back_test_algoritm_tow.py`:
Using resistance support levels as well as getting confirmation using candlestick principles.

## Result
![4492](https://user-images.githubusercontent.com/113052872/236652402-8ef6b6ae-2885-4a22-a3b4-8c1e956ba796.jpg)
![4493](https://user-images.githubusercontent.com/113052872/236652404-54b23cdc-e964-4f9c-9cdc-27bf00027df2.jpg)


### Install The requirements file

```sh
pip3 install -r requirements.txt
```

### Installing TA-Lib
This library helps to implement all principles of candlesticks.
for install talib` library see the link below:
https://pypi.org/project/TA-Lib/


### Download Data
Download the data in the link below:
https://forexsb.com/historical-forex-data




