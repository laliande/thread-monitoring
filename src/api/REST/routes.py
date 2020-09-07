from flask import Blueprint
import ccxt
from flask import Response
from flask import request
from json import dumps
from src.charts.monitoring import get_ohlcv, get_close_values, calculate_EMA, calculate_MACD, calculate_RSI, calculate_SMA, get_one_indicator

api = Blueprint('api', __name__)

exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
indicators = ['RSI', 'MACD', 'SMA', 'EMA']


def add_date_for_indicators(indicat, ohlcv):
    data_chart = []
    for i in range(len(indicat)):
        point = [ohlcv[i][0], indicat[i]]
        data_chart.append(point)
    return data_chart


@api.route('/indicators', methods=['GET'])
def one_indicators():
    symbol = request.args.get('symbol')
    indicator = request.args.get('indicator')
    ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
    indicat = get_one_indicator(indicator, ohlcv)
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
    response = {}
    ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
    for indicat in indicators:
        i = get_one_indicator(indicat, ohlcv)
        i = add_date_for_indicators(i, ohlcv)
        response.update({indicat: i})
    return Response(dumps({'Indicators for {}'.format(symbol): response}))


@api.route('/allCurrency', methods=['GET'])
def all_currency():
    indicator = request.args.get('indicator')
    response = {}
    for symbol in symbols:
        ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
        indicat = get_one_indicator(indicator, ohlcv)
        indicat = add_date_for_indicators(indicat, ohlcv)
        response.update({symbol: indicat})
    return Response(dumps({'{} for all currency'.format(indicator): response}))
