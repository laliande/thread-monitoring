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
symbols = ['LTC/USDT', 'XRP/USDT', 'ETH/USDT', 'BNB/USDT', 'BTC/USDT']
timeframe = '1m'
indicators = ['RSI', 'MACD', 'SMA', 'EMA']
exchange = ccxt.binance()
bot = telebot.TeleBot(token, threaded=False)


def search(query):
    search_params = symbols + indicators
    result = []
    for param in search_params:
        if query.upper() in param and len(query) > 0:
            if param in symbols:
                for indicator in indicators:
                    photo_url = get_photo_url(param, indicator)
                    result.append(
                        {'photo_url': photo_url, 'thumb_url': 'https://res.cloudinary.com/di8exrc5g/image/upload/icons/{}.png'.format(param.split('/')[0] + '/' + indicator)})
            elif param in indicators:
                for symbol in symbols:
                    photo_url = get_photo_url(symbol, param)
                    result.append(
                        {'photo_url': photo_url, 'thumb_url': 'https://res.cloudinary.com/di8exrc5g/image/upload/icons/{}.png'.format(symbol.split('/')[0] + '/' + param)})
    return result


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
        photo_url = get_photo_url(select[0], select[1])
        bot.send_photo(
            message.chat.id, photo_url, reply_markup=answer[1])
    else:
        bot.reply_to(message, answer[0], reply_markup=answer[1])


result_id = 1


@bot.inline_handler(lambda query: len(query.query) >= 0)
def query_photo(inline_query):
    global result_id
    offers = []
    if inline_query.query.upper() in indicators:

        for i in range(len(symbols)):
            photo_url = get_photo_url(symbols[i], inline_query.query.upper())
            print(symbols[i].split('/'))
            r = types.InlineQueryResultPhoto(result_id,
                                             photo_url=photo_url,
                                             thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/icons/{}.png'.format(symbols[i].split('/')[0] + '/' + inline_query.query.upper()), photo_height=200, photo_width=200)
            result_id += 1
            offers.append(r)
    elif inline_query.query.upper() in symbols:

        for i in range(len(indicators)):
            photo_url = get_photo_url(
                inline_query.query.upper(), indicators[i])
            r = types.InlineQueryResultPhoto(result_id,
                                             photo_url=photo_url,
                                             thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/icons/{}.png'.format(inline_query.query.upper().split('/')[0] + '/' + indicators[i]), photo_height=200, photo_width=200)
            result_id += 1
            offers.append(r)

    else:

        founded = search(inline_query.query)

        if len(founded) == 0:

            for i in range(len(indicators)):
                for j in range(len(symbols)):
                    print(symbols[j], indicators[i])
                    photo_url = get_photo_url(symbols[j], indicators[i])
                    r = types.InlineQueryResultPhoto(result_id,
                                                     photo_url=photo_url,
                                                     thumb_url='https://res.cloudinary.com/di8exrc5g/image/upload/icons/{}.png'.format(symbols[j].split('/')[0] + '/' + indicators[i]), photo_height=200, photo_width=200)
                    result_id += 1
                    offers.append(r)
        elif len(founded) > 0:

            for itm in founded:
                r = types.InlineQueryResultPhoto(result_id,
                                                 photo_url=itm['photo_url'],
                                                 thumb_url=itm['thumb_url'], photo_height=200, photo_width=200)
                result_id += 1
                offers.append(r)

    bot.answer_inline_query(inline_query.id, offers, cache_time=0)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
