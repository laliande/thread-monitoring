from flask import Blueprint
import ccxt
from flask import Response
from flask import request
from json import dumps
from src.charts.monitoring import get_ohlcv, get_close_values, calculate_EMA, calculate_MACD, calculate_RSI, calculate_SMA

api = Blueprint('api', __name__)

exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
indicators = ['RSI', 'MACD', 'SMA', 'EMA']


def calculate_indicators(ohlcv):
    close_values = get_close_values(ohlcv)
    sma = calculate_SMA(close_values)
    macd = calculate_MACD(close_values)
    rsi = calculate_RSI(close_values)
    ema = calculate_EMA(close_values)
    indicators_with_dates = []
    for indicator in [sma, macd, rsi, ema]:
        data_chart = add_date_for_indicators(indicator, ohlcv)
        indicators_with_dates.append(data_chart)
    response = [{'SMA': indicators_with_dates[0], 'MACD': indicators_with_dates[1],
                 'RSI': indicators_with_dates[2], 'EMA': indicators_with_dates[3]}]
    return response


def add_date_for_indicators(indicat, ohlcv):
    data_chart = []
    for i in range(len(indicat)):
        point = [ohlcv[i][0], indicat[i]]
        data_chart.append(point)
    return data_chart


@api.route('/indicators', methods=['GET'])
def indicators():
    symbol = request.args.get('symbol')
    indicator = request.args.get('indicator')
    ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
    close_values = get_close_values(ohlcv)
    if indicator == 'SMA':
        indicat = calculate_SMA(close_values)
    elif indicator == 'RSI':
        indicat = calculate_RSI(close_values)
    elif indicator == 'MACD':
        indicat = calculate_MACD(close_values)
    elif indicator == 'EMA':
        indicat = calculate_EMA(close_values)
    data_chart = add_date_for_indicators(indicat, ohlcv)
    return Response(dumps({'points': data_chart}), status=200, mimetype='application/json')


@api.route('/ohlcv', methods=['GET'])
def ohlcv():
    symbol = request.args.get('symbol')
    ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
    return Response(dumps({'candles': ohlcv}))


@api.route('/allIndicators', methods=['GET'])
def all_indicators():
    symbol = request.args.get('symbol')
    ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
    indicators = calculate_indicators(ohlcv)
    return Response(dumps({'indicators': indicators}))
