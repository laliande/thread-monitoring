
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import time
import schedule
import cloudinary.uploader
import cloudinary
from src.conf.config import cloudinary_conf


exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'


def create_graphic(label, symbol):
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    chart_img = create_chart(quotes, format_time, label=label)
    return chart_img


def generation_img():
    charts_img = {}
    for i in range(len(symbols)):
        img = create_graphic(label=symbols[i], symbol=symbols[i])
        charts_img.update({symbols[i]: img})
    return charts_img


def upload_on_cloudinary():
    charts = generation_img()
    for key, value in charts.items():
        cloudinary.uploader.upload(
            value, public_id='charts/' + key.replace('/', '-'))


schedule.every(1).minutes.do(upload_on_cloudinary)


def run_shedule():
    upload_on_cloudinary()
    while True:
        schedule.run_pending()
        time.sleep(1)
