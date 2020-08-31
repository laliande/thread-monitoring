
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import time
import schedule


exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'


def create_graphic(label, symbol):
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    create_chart(quotes, format_time, label=label)


def generation_img():
    for i in range(len(symbols)):
        print(i)
        create_graphic(label=symbols[i], symbol=symbols[i])


schedule.every(1).minutes.do(generation_img)


def run_shedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
