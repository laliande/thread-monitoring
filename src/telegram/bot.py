import base64
from src.conf.config import token
from src.monitoring import get_date_type, get_ohlcv, create_chart
import ccxt
import telebot
import sys
from telebot import types
import time
import requests
from time import time


exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
start_message = 'Thread monitoring bot in binance'
exchange = ccxt.binance()
bot = telebot.TeleBot(token)

get_graphic = types.ReplyKeyboardMarkup()
for symbol in symbols:
    get_graphic.add(symbol)


def create_graphic(label):
    format_time = get_date_type(timeframe)
    quotes = get_ohlcv(exchange, symbol, timeframe)
    create_chart(quotes, format_time, label=label)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, start_message, reply_markup=get_graphic)


@bot.message_handler(content_types=['text'])
def send_photo(message):
    for symbol in symbols:
        if message.text == symbol:
            create_graphic(label=symbol)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            img = open(sys.path[0] + '\\src\\telegram\\chart.png', 'rb')
            bot.send_photo(message.chat.id, img,
                           reply_markup=get_graphic)
            img.close()


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    try:
        offers = []
        for i in range(len(symbols)):
            create_graphic(label=symbols[i])
            photo_url = 'https://aaf85aefabc9.ngrok.io/get-chart/' + \
                str(int(time()))
            thumb_url = 'https://aaf85aefabc9.ngrok.io/get-BTCUSDT/' + \
                str(int(time()))
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
