import telebot
from telebot import types
import time
import whether
from pyowm import OWM
from pyowm.commons.enums import SubscriptionTypeEnum


API_TOKEN = '1935823217:AAEdJYzUGwP465TdzhycGQn41wopqBV5A_o'

bot = telebot.TeleBot(API_TOKEN)
info = bot.get_me()

def config():
    config = {
        'subscription_type': SubscriptionTypeEnum.FREE,
        'language': 'ru',
        'connection': {
            'use_ssl': True,
            'verify_ssl_certs': True,
            'use_proxy': False,
            'timeout_secs': 5
        },
        'proxies': {
            'http': 'http://user:pass@host:port',
            'https': 'socks5://user:pass@host:port'
        }
    }
    return config

API_TOKEN = '1180b504dd3815f626bc826139b04592'
owm = OWM(API_TOKEN, config = config())

whettrrt = {}

""" Класс запроса получения информации о погоде"""
class Whether:

    """ Функция получения погоды по результату поиска города"""
    @staticmethod
    def get_whther_from_name_sity(sity):
        try:
            Weather_man = owm.weather_manager()
            monitoring = Weather_man.weather_at_place(sity)
            weather = monitoring.weather
            status = weather.detailed_status
            return f"В {sity} сейчас {status}, температура воздуха = {(weather.temp['temp'] - 273):.0f}"
        except Exception:
            return None
        
""" Функция получения погоды по результату поиска местоположения (геолокация) """
    @staticmethod
    def get_whther_from_geo_data(lat, lon):
        get_Weather = owm.weather_manager().weather_at_coords(lat, lon)
        place = get_Weather.location.name
        status = get_Weather.weather.detailed_status
        temp = get_Weather.weather.temp
        return f"В {place} сейчас {status}, температура воздуха = {(temp['temp'] - 273):.0f}"

""" Декоратор запуска бота(приветствие), создание кнопок, отправления соответсвующих сообщений """
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

""" Декоратор приема и отправки сообщений """
@bot.message_handler(content_types=['text', 'location'])
def get_txt(message):
    if message.text == 'МОЙ ID':
        bot.send_message(message.chat.id, f"{message.from_user.id}") 
    elif message.text == 'Время':
        bot.send_message(message.chat.id, time.strftime('%H'':''%M'':''%S'))
    elif message.text == 'Погода':
        bot.reply_to(message, f"Отправте свои геоданные, если хотите узнать погоду в другом городе, отправте название "
                              f"города")
        whettrrt[message.chat.id] = True
    elif message.content_type == 'text':
        wet_sity = Whether.get_whther_from_name_sity(message.text)
        if wet_sity is not None and whettrrt[message.chat.id] == True:
            bot.send_message(message.chat.id, wet_sity)
            whettrrt[message.chat.id] = False
        elif wet_sity is not None:
            bot.send_message(message.chat.id, f"Повторите команду запроса погоды")
        elif whettrrt[message.chat.id] == True:
            bot.send_message(message.chat.id, f"Не найден город, повторите ещё раз.")
    elif message.content_type == 'location':
        if whettrrt[message.chat.id] == True:
            latitude = message.location.latitude
            longitude = message.location.longitude
            wet_geo = Whether.get_whther_from_geo_data(latitude, longitude)
            bot.send_message(message.chat.id, wet_geo)
            whettrrt[message.chat.id] = False

bot.polling(none_stop=True, interval=0)


