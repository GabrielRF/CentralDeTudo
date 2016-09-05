import configparser
import datetime
import logging
import logging.handlers
import telebot

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

bot = telebot.TeleBot(bot_token)

def to_line(text):
   with open(line_file, 'a', encoding="utf-8") as file:
       file.write(text + '\n')
       file.close()
   with open(line_file, 'r', encoding="utf-8") as file:
       lines = file.readlines()
       file.close()
       return len(lines) 

def line_qtd():
    with open(line_file, 'r') as file:
        lines = file.readlines()
        file.close()
        return len(lines)

@bot.message_handler(commands=['fila'])
def send_fila(message):
    if message.from_user.username.lower() in bot_admin.lower():
        logger_info.info(str(datetime.datetime.now()) + '\t' + message.from_user.username + '\t' + str(message.text))
        first_line = line_qtd()
        bot.reply_to(message, first_line)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    # print(message.text)
    if message.from_user.username.lower() in bot_admin.lower():
        logger_info.info(str(datetime.datetime.now()) + '\t' + str(message.from_user.username) + '\t' + str(message.text))
        if 'http' in message.text[0:4]:
            line_size = to_line(message.text.split(' ')[0].split('\n')[0])
            bot.reply_to(message, 'Link adicionado à /fila.'
                + '\nNa fila: ' + str(line_size))
        else:
            bot.reply_to(message, 'Link?')

bot.polling()
