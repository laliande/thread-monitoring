from flask import Blueprint
import ccxt
from flask import Response
from flask import request
from json import dumps
from src.charts.monitoring import get_ohlcv, get_close_values, calculate_EMA, calculate_MACD, calculate_RSI, calculate_SMA, get_one_indicator
from flask_restplus import Api, fields, Resource

blueprint = Blueprint('api', __name__)
api = Api(blueprint, doc='/doc/', version='1.0', title='Techniсal Indicators API',
          description='API for obtaining technical indicators for traders')

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
@api.doc(params={'symbol': 'LTC/USDT, XRP/USDT, ETH/USDT, BNB/USDT, BTC/USDT', 'indicator': 'RSI, MACD, SMA,EMA'})
class IndicatorsResource(Resource):
    @api.response(200, 'List of points for plotting')
    def get(self):
        symbol = request.args.get('symbol')
        indicator = request.args.get('indicator')
        ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
        indicat = get_one_indicator(indicator, ohlcv)
        data_chart = add_date_for_indicators(indicat, ohlcv)
        return Response(dumps({'points': data_chart}), status=200, mimetype='application/json')


@api.route('/ohlcv', methods=['GET'])
@api.doc(params={'symbol': 'LTC/USDT, XRP/USDT, ETH/USDT, BNB/USDT, BTC/USDT'})
class OHLCVResource(Resource):
    @api.response(200, 'List of candles for plotting')
    def get():
        symbol = request.args.get('symbol')
        ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
        return Response(dumps({'candles': ohlcv}))


@api.route('/allIndicators', methods=['GET'])
@api.doc(params={'symbol': 'LTC/USDT, XRP/USDT, ETH/USDT, BNB/USDT, BTC/USDT'})
class allIndicatorsResource(Resource):
    @api.response(200, 'List of indicators for the selected currency')
    def get():
        symbol = request.args.get('symbol')
        response = {}
        ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
        for indicat in indicators:
            i = get_one_indicator(indicat, ohlcv)
            i = add_date_for_indicators(i, ohlcv)
            response.update({indicat: i})
        return Response(dumps({'Indicators for {}'.format(symbol): response}))


@api.route('/allCurrency', methods=['GET'])
@api.doc(params={'indicator': 'RSI, MACD, SMA,EMA'})
class allCurrencyResource(Resource):
    @api.response(200, 'List of currency for the selected indicator')
    def get():
        indicator = request.args.get('indicator')
        response = {}
        for symbol in symbols:
            ohlcv = get_ohlcv(exchange, symbol, timeframe, formatdate='unix')
            indicat = get_one_indicator(indicator, ohlcv)
            indicat = add_date_for_indicators(indicat, ohlcv)
            response.update({symbol: indicat})
        return Response(dumps({'{} for all currency'.format(indicator): response}))
