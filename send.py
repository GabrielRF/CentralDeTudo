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

def get_img(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')
    img = html.find('meta', {'property': 'og:image'})
    if not img:
        img = html.find('meta', {'name': 'og:image'})
    try:
        img = img['content']
        preview = False
    except TypeError:
        img = ''
        preview = True
    return preview, img

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
    try:
        title = html.find('meta', {'property': 'og:title'})
        title = title['content']
    except:
        title = html.title.text.strip()
    print(title)
    domain = url.split('://')[1].split('/')[0]
    print(domain)
    preview, img = get_img(url)
    send_msg(title,url,domain,img,preview)

def send_msg(title,url,domain,img,preview):
    message = ('<b>{}</b><a href="{}">.</a>' +
        '\n<a href="{}">{}</a>').format(title,img,url,domain)
    bot.send_message(msg_dest, message, parse_mode='HTML', 
        disable_web_page_preview=preview)

try:
    url = line_read()
    print(url)
    send_line(url)
except:
    pass
