import time

import flask
import requests
import telebot
from telebot import apihelper

import config

TOKEN = config.TOKEN
WEBHOOK_HOST = 'https://unlock.issac.bid'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = ''
WEBHOOK_SSL_PRIV = ''

WEBHOOK_URL_BASE = 'https://{}:{}'.format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/{}/'.format(TOKEN)
# apihelper.proxy = {'https':'socks5://127.0.0.1:10808'}

bot = telebot.TeleBot(TOKEN)

app = flask.Flask(__name__)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

headers = {
        'referer': 'https://nmsl.shadiao.app/?from_chp',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

def get_zuan(params):
    msg = requests.get(
        "https://nmsl.shadiao.app/api.php",
        params=params,
        headers=headers
    )
    return msg

@bot.message_handler(commands=['random'])
def random_zuan(message):
    bot.send_chat_action(message.chat.id, 'typing')
    msg = get_zuan({'level': 'min','lang': 'zh_cn'})
    bot.send_message(message.chat.id, msg.text)

@bot.message_handler(commands=['fuck'])
def random_zuan(message):
    bot.send_chat_action(message.chat.id, 'typing')
    msg = get_zuan({'lang': 'zh_cn'})
    bot.send_message(message.chat.id, msg.text)

bot.remove_webhook()

time.sleep(1)

bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH
)

app.run(
    host='127.0.0.1',
    port=5000
)
