import base64
from src.conf.config import token
import ccxt
import telebot
import sys
from telebot import types
import requests
from time import time, sleep
import cloudinary.api


length = 80
exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
indicators = ['RSI', 'MACD', 'SMA', 'EMA']

start_message = 'Monitoring technial indicators'
exchange = ccxt.binance()
bot = telebot.TeleBot(token, threaded=False)

get_graphic = types.ReplyKeyboardMarkup()
for symbol in symbols:
    get_graphic.add(symbol)


def get_photo_url(symbol, indicator):
    name_chart = (symbol + '-' + indicator).replace('/', '-')
    response = cloudinary.api.resources_by_ids(
        ['charts/{}'.format(name_chart)])
    img = response['resources'][0]['secure_url']
    photo_url = img + '?from={}'.format(str(int(time())))
    return photo_url


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start_message, reply_markup=get_graphic)


@bot.message_handler(content_types=['text'])
def send_photo(message):
    for symbol in symbols:
        if message.text == symbol:
            bot.send_chat_action(message.chat.id, 'upload_photo')
            photo_url = get_photo_url(symbol)
            bot.send_photo(message.chat.id, photo_url,
                           reply_markup=get_graphic)


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    offers = []
    if inline_query.query.upper() in indicators:
        for i in range(len(symbols)):
            photo_url = get_photo_url(symbols[i], inline_query.query.upper())
            r = types.InlineQueryResultPhoto(i,
                                             photo_url=photo_url,
                                             thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/v1598975952/icons/BTN0.5_evirw0.png', photo_height=200, photo_width=200)
            offers.append(r)

    bot.answer_inline_query(inline_query.id, offers, cache_time=0)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
