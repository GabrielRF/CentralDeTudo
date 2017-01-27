import configparser
import datetime
import flask
import logging
import logging.handlers
import random
import telebot
from thumbot import Thumbot
#No polling. Nesse arquivo mesmo
config = configparser.ConfigParser()
config.sections()
config.read('/usr/local/bin/CentralDeTudo/bot.conf')

LOG_INFO_FILE = '/var/log/CentralBot/centralbot.log'
logger_info = logging.getLogger('InfoLogger')
logger_info.setLevel(logging.DEBUG)
handler_info = logging.handlers.RotatingFileHandler(LOG_INFO_FILE,
    maxBytes=10240, backupCount=5, encoding='utf-8')
logger_info.addHandler(handler_info)

bot_token = config['BOT']['token']
msg_dest = config['BOT']['dest']
bot_admin = config['BOT']['admin']
line_file = config['LINE']['file']
urgent_file = config['LINE']['urgent']

webhook_host = config['WEBHOOK']['host']
webhook_port = config['WEBHOOK']['port']
webhook_listen = config['WEBHOOK']['listen']
webhook_ssl_cert = config['WEBHOOK']['ssl_cert']
webhook_ssl_priv = config['WEBHOOK']['ssl_priv']

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(bot_token)
app = flask.Flask(__name__)

WEBHOOK_URL_BASE = "https://%s:%s" % (webhook_host, webhook_port)
WEBHOOK_URL_PATH = "/%s/" % (bot_token)

def to_first_line(text):
    with open(line_file, 'r') as original: data = original.read()
    with open(line_file, 'w') as modified: modified.write(text + '\n' + data)
    pop_last()

def to_line(text):
    with open(line_file, 'a', encoding="utf-8") as file:
        file.write(text + '\n')
        file.close()
    with open(line_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        file.close()
        return len(lines) 

def pop_last():
    with open(line_file, 'r') as file:
        lines = file.readlines()
    lines.pop(len(lines)-1)
    with open(line_file, 'w') as file:
        for l in lines:
            file.write(l)

def in_file(text):
    lines = open(line_file, 'r')
    for line in lines:
        if text in line:
            pop_last()

def line_qtd():
    with open(line_file, 'r') as file:
        lines = file.readlines()
        file.close()
        return len(lines)

def urgent_answer():
    falas = open(urgent_file).read().splitlines()
    fala = random.choice(falas)
    return fala

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username.lower() in bot_admin.lower():
        bot.reply_to(message, 'Olá!')

@bot.message_handler(commands=['fila'])
def send_fila(message):
    if message.from_user.username.lower() in bot_admin.lower():
        logger_info.info(str(datetime.datetime.now()) + '\t' + message.from_user.username + '\t' + str(message.text))
        first_line = line_qtd()
        bot.reply_to(message, first_line)

@bot.message_handler(commands=['urgente'])
def urgent(message):
    if message.from_user.username.lower() in bot_admin.lower():
        logger_info.info(str(datetime.datetime.now()) + '\t' + message.from_user.username + '\t' + str(message.text))
        msg = bot.reply_to(message, urgent_answer())
        bot.register_next_step_handler(msg, send_urgent)

def send_urgent(message):
    if message.from_user.username.lower() in bot_admin.lower():
        logger_info.info(str(datetime.datetime.now()) + '\t' + message.from_user.username + '\t' + str(message.text))
        to_first_line(message.text.split(' ')[0].split('\n')[0])

@bot.callback_query_handler(lambda q: q.data == 'thumb_up')
def thumb_up(callback):

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    thumbot = Thumbot(chat_id, message_id)

    print('thumb up +1: ')
    print('chat_id: ', chat_id)
    print('message_id: ', message_id)
    print('ups: ', thumbot.ups)
    print('downs: ', thumbot.downs)
    print()
    if thumbot.up(callback.from_user.id):
        bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=thumbot.keyboard())


@bot.callback_query_handler(lambda q: q.data == 'thumb_down')
def thumb_down(callback):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    thumbot = Thumbot(chat_id, message_id)
    print('thumb down +1')
    print('chat_id: ', chat_id)
    print('message_id: ', message_id)
    print('user_id: ', callback.from_user.id)
    print('ups: ', thumbot.ups)
    print('downs: ', thumbot.downs)
    print()
    if thumbot.down(callback.from_user.id):
        bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=thumbot.keyboard())

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Ok')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.from_user.username.lower() in bot_admin.lower():
        logger_info.info(str(datetime.datetime.now()) + '\t' + str(message.from_user.username) + '\t' + str(message.text))
        if 'http' in message.text[0:4]:
            line_size = to_line(message.text.split(' ')[0].split('\n')[0])
            bot.reply_to(message, 'Link adicionado a fila.'
                + '\nNa fila: ' + str(line_size))
        else:
            bot.reply_to(message, 'Link?')



bot.remove_webhook()
#bot.polling()

print(WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
    certificate=open(webhook_ssl_cert, 'r'))
app.run(host=webhook_listen,
    port=int(webhook_port),
        ssl_context=(webhook_ssl_cert, webhook_ssl_priv),
        debug=True)
