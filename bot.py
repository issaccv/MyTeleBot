import telebot
import requests
import config
from telebot import apihelper

TOKEN = config.TOKEN

# apihelper.proxy = {'https':'socks5://127.0.0.1:10808'}

bot = telebot.TeleBot(TOKEN)

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

bot.polling()