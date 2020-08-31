import ccxt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib
import sys
matplotlib.use('agg')


def get_ohlcv(exchange, symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe)
    for i in range(len(ohlcv)):
        tz = 'Europe/Moscow'
        ohlcv[i][0] = int(ohlcv[i][0]//1000) + 10800
        ohlcv[i][0] = datetime.utcfromtimestamp(
            ohlcv[i][0]).strftime('%Y-%m-%d %H:%M:%S')
        ohlcv[i][0] = mdates.date2num(ohlcv[i][0])
    return ohlcv


def create_chart(quotes, format, label):
    fig, ax = plt.subplots()
    candlestick_ohlc(ax, quotes[-80:], width=0.0003,
                     colorup='#9933FF', colordown='white')
    plt.plot(color='white')
    plt.style.use("dark_background")
    plt.title(label, color='grey')

    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('grey')
    ax.spines['top'].set_color('grey')
    ax.spines['right'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.tick_params(color='grey', labelcolor='grey')

    ax.xaxis.set_major_formatter(mdates.DateFormatter(format))
    ax.xaxis_date()

    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)

    plt.grid(color='grey', linestyle=':', linewidth=0.5)
    name_image = label.replace('/', '-')
    plt.savefig(sys.path[0] + '\\src\\img\\{}.png'.format(name_image))
    plt.close(fig=fig)


def get_date_type(timeframe):
    if timeframe[-1] == 'h':
        format_time = '%d %H:%M'
    elif timeframe[-1] == 'm':
        format_time = '%H:%M'
    elif timeframe[-1] == 'd':
        format_time = '%D'
    return format_time
