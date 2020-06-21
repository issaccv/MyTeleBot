import time
import re
import flask
import requests
import telebot
from telebot import apihelper

import config

TOKEN = config.TOKEN
IP_TOKEN = config.IP_TOKEN


WEBHOOK_URL_BASE = "https://{}:{}".format(config.WEBHOOK_HOST, config.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TOKEN)
# apihelper.proxy = {'https':'socks5://127.0.0.1:10808'}

bot = telebot.TeleBot(TOKEN)

app = flask.Flask(__name__)


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


headers = {
    "referer": "https://nmsl.shadiao.app/?from_chp",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}


def get_zuan(params):
    msg = requests.get(
        "https://nmsl.shadiao.app/api.php", params=params, headers=headers
    )
    return msg


@bot.message_handler(commands=["random"])
def random_zuan(message):
    bot.send_chat_action(message.chat.id, "typing")
    msg = get_zuan({"level": "min", "lang": "zh_cn"})
    bot.send_message(message.chat.id, msg.text)


@bot.message_handler(commands=["fuck"])
def random_zuan(message):
    bot.send_chat_action(message.chat.id, "typing")
    msg = get_zuan({"lang": "zh_cn"})
    bot.send_message(message.chat.id, msg.text)


@bot.message_handler(commands=["ip"])
def get_ipinfo(message):
    bot.send_chat_action(message.chat.id, "typing")
    api_url = "https://ipinfo.io/json/"
    try:
        ip = message.chat.text.split()[1]
        p = re.compile(
            "^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$"
        )
        m = p.match(ip)
        if m:
            params = {"token": IP_TOKEN}
            r = requests.get(api_url + m.group(), params=params).json()

            def info(data):
                t = []
                for k, v in data.items():
                    if k == "asn":
                        pass
                    else:
                        t.append(k + ":" + v)
                for k, v in data["asn"].items():
                    t.append(k + ":" + v)
                message = "\n".join(t)
                return message

            info = info(r)
            bot.send_message(message.chat.id, info)
    except:
        bot.send_message(message.chat.id, "Require Valid IP")


bot.remove_webhook()

time.sleep(2)

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app.run(host="127.0.0.1", port=5000)
