import telebot
from telebot import types
import time
import whether


API_TOKEN = '1935823217:AAEdJYzUGwP465TdzhycGQn41wopqBV5A_o'

bot = telebot.TeleBot(API_TOKEN)
info = bot.get_me()


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def get_user_info(message):
    main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_name = types.KeyboardButton('МОЙ ID')
    item_time = types.KeyboardButton('Время')
    item_whether = types.KeyboardButton('Погода')
    main_menu.add(item_name, item_time, item_whether)
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}, '
                                      f'какую информацию вы желаете получить?', reply_markup=main_menu)
    print(f"{message.from_user.first_name} {message.from_user.last_name} начала использовать бота")


@bot.message_handler(content_types=['text', 'location'])
def get_txt(message):
    if message.text == 'МОЙ ID':
        bot.send_message(message.chat.id, f"{message.from_user.id}")
    elif message.text == 'Время':
        bot.send_message(message.chat.id, time.strftime('%H'':''%M'':''%S'))
    elif message.text == 'Погода':
        bot.reply_to(message, f"Отправте свои геоданные, если хотите узнать погоду в другом городе, отправте название "
                              f"города")
        whether.whettrrt[message.chat.id] = True
        print(f'{message.from_user.first_name} {message.from_user.last_name} получил запрос на погоду, {whether.whettrrt[message.chat.id]}')
    elif message.content_type == 'text':
        wet_sity = whether.Whether.get_whther_from_name_sity(message.text)
        if wet_sity is not None and whether.whettrrt[message.chat.id] == True:
            bot.send_message(message.chat.id, wet_sity)
            whether.whettrrt[message.chat.id] = False
            print(f'{message.from_user.first_name} {message.from_user.last_name} ввел город {whether.whettrrt[message.chat.id]}')
        elif wet_sity is not None:
            bot.send_message(message.chat.id, f"Повторите команду запроса погоды")
        elif whether.whettrrt[message.chat.id] == True:
            bot.send_message(message.chat.id, f"Не найден город, повторите ещё раз.")
    elif message.content_type == 'location':
        if whether.whettrrt[message.chat.id] == True:
            latitude = message.location.latitude
            longitude = message.location.longitude
            wet_geo = whether.Whether.get_whther_from_geo_data(latitude, longitude)
            bot.send_message(message.chat.id, wet_geo)
            whether.whettrrt[message.chat.id] = False

bot.polling(none_stop=True, interval=0)
