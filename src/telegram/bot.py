import base64
from src.conf.config import token
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import telebot
import sys
from telebot import types
import requests
from time import time


exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
start_message = 'Thread monitoring bot in binance'
exchange = ccxt.binance()
bot = telebot.TeleBot(token, threaded=False)
server_url = 'https://55de5d60cb8c.ngrok.io/'

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
            img = open(
                sys.path[0] + '\\src\\img\\{}.png'.format(symbol.replace('/', '-')), 'rb')
            bot.send_photo(message.chat.id, img,
                           reply_markup=get_graphic)
            img.close()


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    try:
        offers = []
        for i in range(len(symbols)):
            photo_url = server_url + 'get-chart/' + \
                symbols[i].replace('/', '-') + '/' + str(int(time()))
            thumb_url = server_url + 'get-BTCUSDT/' + \
                symbols[i].replace('/', '-')
            print(photo_url)
            print(thumb_url)
            r = types.InlineQueryResultPhoto(i,
                                             photo_url=photo_url,
                                             thumb_url=thumb_url, photo_height=200, photo_width=200)
            offers.append(r)
        bot.answer_inline_query(inline_query.id, offers, cache_time=0)
    except Exception as e:
        print(e)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
