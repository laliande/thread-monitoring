import ccxt
from datetime import datetime
import matplotlib.dates as mdates


def get_ohlcv(exchange, symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe)
    for i in range(len(ohlcv)):
        ohlcv[i][0] = datetime.utcfromtimestamp(
            int(ohlcv[i][0]//1000)).strftime('%Y-%m-%d %H:%M:%S')
        ohlcv[i][0] = mdates.date2num(ohlcv[i][0])
    return ohlcv
