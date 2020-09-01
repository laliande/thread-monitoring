import base64
from src.conf.config import token
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import telebot
import sys
from telebot import types
import requests
from time import time, sleep
from src.conf.config import db


exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
start_message = 'Thread monitoring bot in binance'
exchange = ccxt.binance()
bot = telebot.TeleBot(token, threaded=False)
server_url = 'https://edf18a1b85c1.ngrok.io'

get_graphic = types.ReplyKeyboardMarkup()
for symbol in symbols:
    get_graphic.add(symbol)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start_message, reply_markup=get_graphic)


@bot.message_handler(content_types=['text'])
def send_photo(message):
    for symbol in symbols:
        if message.text == symbol:
            bot.send_chat_action(message.chat.id, 'upload_photo')
            photo_url = db.get(symbol).decode('utf-8') + \
                '?from={}'.format(str(int(time())))
            bot.send_photo(message.chat.id, photo_url,
                           reply_markup=get_graphic)


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    try:
        offers = []
        for i in range(len(symbols)):
            photo_url = db.get(symbols[i]).decode('utf-8') + \
                '?from={}'.format(str(int(time())))
            r = types.InlineQueryResultPhoto(i,
                                             photo_url=photo_url,
                                             thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/v1598975952/icons/BTN0.5_evirw0.png', photo_height=200, photo_width=200)
            offers.append(r)

        bot.answer_inline_query(inline_query.id, offers,
                                cache_time=0)
    except Exception as e:
        print(e)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
