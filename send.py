from bs4 import BeautifulSoup
import configparser
import random
import requests
import telebot
import sys

config = configparser.ConfigParser()
config.sections()
config.read('/usr/local/bin/CentralDeTudo/bot.conf')

bot_token = config['BOT']['token']
msg_dest = config['BOT']['dest']
bot_admin = config['BOT']['admin']
line_file = config['LINE']['file']

bot = telebot.TeleBot(bot_token)

def line_read():
    with open(line_file, 'r', encoding="utf-8") as file:
        first_line = file.readline()
        lines = file.readlines()
        file.close()
    with open(line_file, 'w', encoding="utf-8") as file:
        for l in lines:
            file.write(l)
        file.close()
    lines = open(line_file).readlines()
    random.shuffle(lines)
    open(line_file, 'w', encoding="utf-8").writelines(lines)
    return first_line.strip()

def send_line(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    title = html.title.text.strip()
    print(title)
    domain = url.split('://')[1].split('/')[0]
    print(domain)
    send_msg(title,url,domain)

def send_msg(title,url,domain):
    message = ('<b>{}</b>' +
        '\n<a href="{}">{}</a>').format(title,url,domain)
    bot.send_message(msg_dest, message, parse_mode='HTML', 
        disable_web_page_preview=False)

try:
    url = line_read()
    send_line(url)
except:
    pass
