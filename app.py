import telebot
import requests
import json

TOKEN = '5950939460:AAHqveoXbNgQw0yccdKO8BwqhOuc3gOYo4s'

bot = telebot.TeleBot(TOKEN)

keys = {
    'биток' : 'BTC',
    'доллары': 'USD',
    'эфир': 'ETH'

}


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '''
    Данный бот делает конвертацию из одной валюты в другую.
Впишите запрос в формате:

<Имя Валюты> <В какую валюту перевести> <Количество>


Увидеть список всех доступных валют:  /values
    '''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text. split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote.lower()]}&tsyms={keys[base.lower()]}')

    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)





bot.polling()