import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])        # Стартовое сообщение и ответ при командах /start и /help
def help(message: telebot.types.Message):
    text = '''
    Данный бот делает конвертацию из одной валюты в другую.
Впишите запрос в формате:

<Имя Валюты> <В какую валюту перевести> <Количество>


Увидеть список всех доступных валют:  /values
    '''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])               # Вывод доступных валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])            # Основная обработка запросов
def convert(message: telebot.types.Message):
    try:
        vals = message.text.split(' ')

        if len(vals) != 3:
            raise APIException('Количество параметров должно быть три')

        quote, base, amount = vals
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)





bot.polling()       # Запускаем бот