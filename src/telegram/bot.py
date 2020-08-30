import base64
from src.conf.config import token, key_imgbb
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import telebot
import sys
from telebot import types
import time
import requests
import cloudinary.uploader
from src.conf.config import cloudinary_config
import random


exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1m'
start_message = 'thread monitoring bot BTC/USDT in binance'
exchange = ccxt.binance()
bot = telebot.TeleBot(token)

get_graphic = types.ReplyKeyboardMarkup()
get_graphic.add('BTC/USDT')

cloudinary.config(
    cloud_name=cloudinary_config['cloud_name'],
    api_key=cloudinary_config['api_key'],
    api_secret=cloudinary_config['api_secret']
)


def create_graphic():
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    create_chart(quotes, format_time)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start_message, reply_markup=get_graphic)


@bot.message_handler(content_types=['text'])
def send_photo(message):
    if message.text.lower() == 'btc/usdt':
        create_graphic()
        bot.send_chat_action(message.chat.id, 'upload_photo')
        img = open(sys.path[0] + '\\src\\telegram\\chart.png', 'rb')
        bot.send_photo(message.chat.id, img,
                       reply_markup=get_graphic)
        img.close()


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    try:
        create_graphic()
        photo_url = 'https://aaf85aefabc9.ngrok.io/get-chart/' + \
            str(random.randint(0, 100))
        thumb_url = 'https://aaf85aefabc9.ngrok.io/get-BTCUSDT/' + \
            str(random.randint(0, 100))
        r = types.InlineQueryResultPhoto('1',
                                         photo_url=photo_url,
                                         thumb_url=thumb_url, photo_height=200, photo_width=200)
        bot.answer_inline_query(inline_query.id, [r], cache_time=0)

    except Exception as e:
        print(e)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
