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


@api.route('/indicators', methods=['GET'])
def get_indicators():
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
    data_chart = []
    for i in range(len(indicat)):
        point = [ohlcv[i][0], indicat[i]]
        data_chart.append(point)
    return Response(dumps({'points': data_chart}), status=200, mimetype='application/json')


@api.route('/ohlcv', methods=['GET'])
def ohlcv():
    symbol = request.args.get('symbol')
    ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
    return Response(dumps({'candles': ohlcv}))
