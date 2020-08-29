import base64
from src.conf.config import token, key_imgbb
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import telebot
import sys
from telebot import types
import time
import requests
exchange = ccxt.binance()

symbol = 'BTC/USDT'
timeframe = '1m'
start_message = 'thread monitoring bot BTC/USDT in binance'
exchange = ccxt.binance()
bot = telebot.TeleBot(token)


def create_graphic():
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    create_chart(quotes, format_time)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start_message)


def uploadphoto():
    with open(sys.path[0] + '\\src\\telegram\\chart.png', "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": key_imgbb,
            "image": base64.b64encode(file.read()),
        }
        response = requests.post(url, payload)
        if response.status_code == 200:
            return {"photo_url": response.json()["data"]["url"], "thumb_url": response.json()["data"]["thumb"]["url"]}
    return None


create_graphic()
img = uploadphoto()


@bot.inline_handler(lambda query: query.query == 'BTC/USDT')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                         img["photo_url"],
                                         img["thumb_url"], photo_width=400, photo_height=400)
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception as e:
        print(e)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


try:
    main_loop()
except KeyboardInterrupt:
    print('\nExiting by user request.\n')
    sys.exit(0)
