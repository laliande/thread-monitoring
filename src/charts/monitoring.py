from matplotlib.pyplot import gca
from flask import Flask
from flask import send_file, make_response, Response
import ccxt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib
import io
import base64
import cloudinary.uploader
import sys
import numpy
import pandas as pd
import math as m
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from pyti.relative_strength_index import relative_strength_index as rsi
import numpy as np
from src.charts.chart_styles import title_font, title_color, title_size, color_up, color_down, width_candle, line_color, grid_color, ax_font, grid_alpha, grid_linewidth, grid_color
matplotlib.use('Agg')


def get_ohlcv(exchange, symbol, timeframe):
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe)
    for i in range(len(ohlcv)):
        tz = 'Europe/Moscow'
        ohlcv[i][0] = int(ohlcv[i][0]//1000) + 10800
        ohlcv[i][0] = datetime.utcfromtimestamp(
            ohlcv[i][0]).strftime('%Y-%m-%d %H:%M:%S')
        ohlcv[i][0] = mdates.date2num(ohlcv[i][0])
    return ohlcv


def get_close_values(ohlcv):
    close_index = 4
    close_values = [x[close_index] for x in ohlcv]
    return close_values


def calculate_SMA(close_values):
    period = 3
    result = sma(close_values, period)
    return result


def calculate_RSI(close_values):
    period = 9
    result = rsi(close_values, period)
    return result


def calculate_MACD(close_values):
    short_period = 12
    long_period = 26
    result = macd(data=close_values, short_period=short_period,
                  long_period=long_period)
    return result


def calculate_EMA(close_values):
    period = 2
    result = ema(close_values, period)
    return result


def disign_chart(label):
    plt.title(label, color=title_color,
              fontproperties=title_font, size=title_size)
    plt.style.use("dark_background")
    plt.plot(color='white')


def create_candle_chart(ax, data):
    candlestick_ohlc(ax, data, colorup=color_up,
                     colordown=color_down, width=width_candle)


def save_chart(label, fig):
    name_image = label.replace('/', '-')
    plot_IObytes = io.BytesIO()
    plt.savefig(plot_IObytes,  format='png', dpi=200)
    plot_IObytes.seek(0)
    plot_hash = base64.b64encode(plot_IObytes.read()).decode('utf8')
    plt.close(fig=fig)
    return 'data:image/jpeg;base64,' + plot_hash


def disign_ax(axes, format):
    for ax in axes:
        ax.set_facecolor('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.grid(color=grid_color, linewidth=grid_linewidth, alpha=grid_alpha)
        for tick in ax.get_xticklabels():
            tick.set_fontproperties(ax_font)
        for tick in ax.get_yticklabels():
            tick.set_fontproperties(ax_font)
        ax.tick_params(axis='both', which='both',
                       labelsize=8, color='grey', labelcolor='grey', left=False, right=False, top=False, bottom=False)
        ax.xaxis.set_major_formatter(mdates.DateFormatter(format))
        ax.xaxis_date()


def plot_oscillo_chart(data, indicator, format, label):
    dates_for_oscillo = []
    for elem in data:
        dates_for_oscillo.append(elem[0])
    fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
    disign_chart(label)
    plt.tight_layout(pad=3, h_pad=1, w_pad=1)
    create_candle_chart(ax1, data)
    ax2.plot(dates_for_oscillo, indicator, color=line_color)
    disign_ax([ax1, ax2], format)
    img = save_chart(label, fig)
    return img


def plot_chart(data, indicator, format, label):
    fig, ax1 = plt.subplots()
    create_candle_chart(ax1, data)
    disign_chart(label)
    ax2 = ax1.twiny()
    ax2.plot(indicator, color=line_color)
    ax2.axis('off')
    disign_ax([ax1], format)
    img = save_chart(label, fig)
    return img


def get_date_type(timeframe):
    if timeframe[-1] == 'h':
        format_time = '%d %H:%M'
    elif timeframe[-1] == 'm':
        format_time = '%H:%M'
    elif timeframe[-1] == 'd':
        format_time = '%D'
    return format_time


def create_graphic(length, exchange, symbol, timeframe, indicator):
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    close_values = get_close_values(quotes)
    if indicator == 'SMA':
        indicat = calculate_SMA(close_values)
    elif indicator == 'RSI':
        indicat = calculate_RSI(close_values)
    elif indicator == 'MACD':
        indicat = calculate_MACD(close_values)
    elif indicator == 'EMA':
        indicat = calculate_EMA(close_values)
    if indicator == 'MACD' or indicator == 'RSI':
        chart = plot_oscillo_chart(
            quotes[-length:], indicat[-length:], format_time, symbol + ' ' + indicator)
    elif indicator == 'SMA' or indicator == 'EMA':
        chart = plot_chart(
            quotes[-length:], indicat[-length:], format_time, symbol + ' ' + indicator)

    return chart


# length = 80
# exchange = ccxt.binance()
# symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
# timeframe = '1m'
# indicators = ['RSI', 'MACD', 'SMA', 'EMA']
# chart = create_graphic(80, exchange, symbols[2], timeframe, indicators[2])
# print(chart)
