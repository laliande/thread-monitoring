
from src.charts.monitoring import create_graphic
import ccxt
import time
import schedule
import cloudinary.uploader
import cloudinary
from src.conf.config import cloudinary_conf

length = 80
exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
indicators = ['RSI', 'MACD', 'SMA', 'EMA']


def generation_img():
    charts_img = {}
    for i in range(len(symbols)):
        for j in range(len(indicators)):
            chart = create_graphic(
                length=length, exchange=exchange, symbol=symbols[i], timeframe=timeframe, indicator=indicators[j])
            charts_img.update({symbols[i] + '-' + indicators[j]: chart})
    return charts_img


def upload_on_cloudinary():
    charts = generation_img()
    for key, value in charts.items():
        response = cloudinary.uploader.upload(
            value, public_id='charts/' + key.replace('/', '-'), invalidate=True)


schedule.every(1).minutes.do(upload_on_cloudinary)


def run_shedule():
    upload_on_cloudinary()
    while True:
        schedule.run_pending()
        time.sleep(1)
