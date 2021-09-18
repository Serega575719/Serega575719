from pyowm import OWM
from pyowm.commons.enums import SubscriptionTypeEnum

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


class Whether:

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

    @staticmethod
    def get_whther_from_geo_data(lat, lon):
        get_Weather = owm.weather_manager().weather_at_coords(lat, lon)
        place = get_Weather.location.name
        status = get_Weather.weather.detailed_status
        temp = get_Weather.weather.temp
        return f"В {place} сейчас {status}, температура воздуха = {(temp['temp'] - 273):.0f}"

