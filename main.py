import requests
import datetime
from pprint import pprint

open_weather_token = 'a9baa1b5867ce5d367c2caf502acc11b'
def get_weather(city, open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        # pprint(data)

        city = data['name']

        weather_descript = data['weather'][0]['main']
        if weather_descript in code_to_smile:
            wd = code_to_smile[weather_descript]
        else:
            pass
            # print('Посмотри в окно сам :)')

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        # print(f"Текущее время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        #       f"Погода в городе: {city}\nТемпература: {temp}C° {wd}\n"
        #       f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
        #       f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
        #       f"Хорошего дня!"
        #       )

    except Exception:
        pass

