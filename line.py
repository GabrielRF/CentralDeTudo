import configparser
import telebot

config = configparser.ConfigParser()
config.sections()
config.read('/usr/local/bin/CentralDeTudo/bot.conf')

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

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.from_user.username.lower() in bot_admin.lower():
        line_size = to_line(message.text)
        bot.reply_to(message, 'Link adicionado à fila.'
            + '\nNa fila: ' + str(line_size))

bot.polling(none_stop=True)
