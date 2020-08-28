import ccxt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib
matplotlib.use('agg')


def get_ohlcv(exchange, symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe)
    for i in range(len(ohlcv)):
        ohlcv[i][0] = datetime.utcfromtimestamp(
            int(ohlcv[i][0]//1000)).strftime('%Y-%m-%d %H:%M:%S')
        ohlcv[i][0] = mdates.date2num(ohlcv[i][0])
    return ohlcv


def create_chart(quotes, format):
    fig, ax = plt.subplots()
    candlestick_ohlc(ax, quotes[-80:], width=0.0003,
                     colorup='green', colordown='white')
    ax.set_facecolor('#16151A')
    ax.xaxis.set_major_formatter(mdates.DateFormatter(format))
    ax.xaxis_date()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.grid(color='grey', linestyle=':', linewidth=0.5)
    plt.savefig('chart.png')


def get_date_type(timeframe):
    if timeframe[-1] == 'h':
        format_time = '%d %H:%M'
    elif timeframe[-1] == 'm':
        format_time = '%H:%M'
    elif timeframe[-1] == 'd':
        format_time = '%D'
    return format_time
