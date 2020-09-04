import base64
from src.conf.config import token
import ccxt
import telebot
import sys
from telebot import types
import requests
from time import time, sleep
import cloudinary.api
from src.telegram.handler_screens import get_next_screen, get_user_select


length = 80
exchange = ccxt.binance()
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
indicators = ['RSI', 'MACD', 'SMA', 'EMA']

start_message = 'Monitoring technial indicators'
exchange = ccxt.binance()
bot = telebot.TeleBot(token, threaded=False)


def get_photo_url(symbol, indicator):
    name_chart = (symbol + '-' + indicator).replace('/', '-')
    response = cloudinary.api.resources_by_ids(
        ['charts/{}'.format(name_chart)])
    img = response['resources'][0]['secure_url']
    photo_url = img + '?from={}'.format(str(int(time())))
    return photo_url


@bot.message_handler(commands=['start'])
def send_welcome(message):
    answer = get_next_screen(message.from_user.id, message.text)
    bot.reply_to(message, answer[0], reply_markup=answer[1])


@bot.message_handler(content_types=['text'])
def send_photo(message):
    answer = get_next_screen(message.from_user.id, message.text)
    if answer[0] == 'photo':
        select = get_user_select(message.from_user.id)
        print(select)
        photo_url = get_photo_url(select[0], select[1])
        bot.send_photo(
            message.chat.id, photo_url, reply_markup=answer[1])
    else:
        bot.reply_to(message, answer[0], reply_markup=answer[1])


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    offers = []

    if inline_query.query.upper() in indicators:
        result_id = 1
        for i in range(len(symbols)):
            photo_url = get_photo_url(symbols[i], inline_query.query.upper())
            r = types.InlineQueryResultPhoto(result_id,
                                             photo_url=photo_url,
                                             thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/v1598975952/icons/BTN0.5_evirw0.png', photo_height=200, photo_width=200)
            result_id += 1
            offers.append(r)
    elif inline_query.query.upper() in symbols:
        result_id = 1
        for i in range(len(indicators)):
            photo_url = get_photo_url(
                inline_query.query.upper(), indicators[i])
            r = types.InlineQueryResultPhoto(result_id,
                                             photo_url=photo_url,
                                             thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/v1598975952/icons/BTN0.5_evirw0.png', photo_height=200, photo_width=200)
            result_id += 1
            offers.append(r)
    else:
        result_id = 1
        for i in range(len(indicators)):
            for j in range(len(symbols)):
                photo_url = get_photo_url(symbols[j], indicators[i])
                r = types.InlineQueryResultPhoto(result_id,
                                                 photo_url=photo_url,
                                                 thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/v1598975952/icons/BTN0.5_evirw0.png', photo_height=200, photo_width=200)
                result_id += 1
                offers.append(r)

    bot.answer_inline_query(inline_query.id, offers, cache_time=0)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
