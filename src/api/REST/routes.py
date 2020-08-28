from flask import Blueprint
from ...monitoring import get_ohlcv, create_chart, get_date_type
import ccxt
from flask import Response
from flask import request
from json import dumps

api = Blueprint('api', __name__)


@api.route('/indicators', methods=['GET'])
def index():
    # for binance
    exchange = ccxt.binance()
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe')
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    create_chart(quotes, format_time)
    return Response(dumps({'response': 'ok'}), status=200, mimetype='application/json')
