import telebot
from config import tickers, TOKEN
from extensions import APIException, CryptoConverter
from telebot import types

currencies = ['KZT', 'USD', 'EUR', 'RUB']

def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttons = []
    for val in currencies:
        if val != base:
            buttons.append(types.KeyboardButton(val))

    markup.add(*buttons)


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])        # Стартовое сообщение и ответ при командах /start и /help
def help(message: telebot.types.Message):
    text = '''
    Данный бот делает конвертацию из одной валюты в другую. Для конвертации отправьте сообщение 
/convert или кликните на эту ссылку.
    '''
    bot.reply_to(message, text)


# @bot.message_handler(commands=['values'])               # Вывод доступных валют. Нет необх, т.к. введены кнопки
# def values(message: telebot.types.Message):
#     text = 'Доступные валюты:'
#     for i in tickers:
#         text = '\n'.join((text, i))
#     bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать'
    # print('reply_markup 1')
    bot.send_message(message.chat.id, text, reply_markup = create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text
    text = 'Выберите валюту, в которую конвертировать'
    # print('reply_markup 2')
    bot.send_message(message.chat.id, text, reply_markup = create_markup(base))
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text
    text = 'Введите количество'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        converted = CryptoConverter.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'{amount} {base} is equal to {converted} {sym}.'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])            # Основная обработка запросов
def convert(message: telebot.types.Message):
    try:
        vals = message.text.split(' ')

        if len(vals) != 3:
            raise APIException('Количество параметров должно быть три')

        quote, base, amount = [i.upper() for i in vals]
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Конвертация {float(amount):,.2f} {quote} = {total_base:,.2f} {base}'
        bot.send_message(message.chat.id, text)





bot.polling()       # Запускаем бот