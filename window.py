from tkinter import *
from pprint import pprint
from tkinter import Canvas
from tkinter import messagebox
from PIL import ImageTk, Image
from icrawler.builtin import GoogleImageCrawler
from geopy import *

import sqlite3
import time
import os
import psw_check
import datetime
import requests
import wikipedia

open_weather_token = 'a9baa1b5867ce5d367c2caf502acc11b'

# 123412341234Af

root = Tk()  # создание окна, его названия и размеры
root.title('Авторизация')
root.geometry('600x400+650+350')
root.resizable(width=False, height=False)

login = StringVar()  # для получения строки из Entry()
password1 = StringVar()
password_reg = StringVar()
registr1 = StringVar()
enter_city = StringVar()

#-------------------
database = sqlite3.connect('database.db')
cursor = database.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users ( 
        login TEXT, 
        password TEXT
    )''')
database.commit()
#-------------------

def parsing_photo(city):
    if os.path.exists('C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos/000001.jpg'):
        os.remove('C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos/000001.jpg')
    google_crawler = GoogleImageCrawler(storage=dict(
        root_dir='C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos'))
    filters = dict(size='medium')
    google_crawler.crawl(keyword=city, max_num=1, filters=filters)


def weather_success(weather_info):
    root_weather = Toplevel(root_main)
    root_weather.title('Погода')
    root_weather.geometry('400x250+750+450')  # сделать ограничение ширины текста как-нибудь
    root_weather.resizable(width=False, height=False)

    weather_label = Label(root_weather, bg='lightgreen', font='Colibri 10', text=weather_info)
    weather_label.pack(pady=5)


def get_weather(city, open_weather_token):
    global wd
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
        pprint(data)

        city = data['name']

        weather_descript = data['weather'][0]['main']
        if weather_descript in code_to_smile:
            wd = code_to_smile[weather_descript]
        else:
            print('Посмотри в окно сам :)')

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        weather_info = f"Текущее время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} по UTC +3\n\
        Погода в городе: {city}\n\
        Температура: {temp}C° {wd}\n\
        Влажность: {humidity}%\n\
        Давление: {pressure} мм.рт.ст\n\
        Ветер: {wind} м/с\n\
        Восход солнца: {sunrise_timestamp}\n\
        Закат солнца: {sunset_timestamp}\n\
        Хорошего дня!"

        weather_success(weather_info)
    except:
        any_fail()


def photo_root():
    root_photo = Toplevel(root_main)
    root_photo.title('Фотография')

    try:
        old_file = os.path.join("C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos", "000001.png")
        new_file = os.path.join("C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos", "000001.jpg")
        os.rename(old_file, new_file)
        print('Формат фото изменен успешно')
    except:
        pass

    tk_pil_img = ImageTk.PhotoImage(Image.open("photos/000001.jpg"))

    canvas = Canvas(root_photo, width=tk_pil_img.width(), height=tk_pil_img.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor=NW, image=tk_pil_img)

    root_photo.mainloop()

def wiki_info_success(wiki_info):
    messagebox.showinfo('Краткая информация', wiki_info)
def any_fail():
    messagebox.showerror('Ошибка поиска', 'Город не найден')

def show_photos(event):
    city = enter_city.get()
    try:
        parsing_photo(city)
        time.sleep(5)
        photo_root()
    except:
        pass


def weather_search(event):
    city = enter_city.get()
    get_weather(city, open_weather_token)

def geo_success(address, coordinates):
    geo_root = Toplevel(root_main)
    geo_root.title('Координаты')
    geo_root.geometry('900x300+500+400')
    geo_root.resizable(width=False, height=False)

    geo_label = Label(geo_root, bg='lightgreen', font='Colibri 10', text=address)
    geo_label.pack(pady=10)

    coords_label = Label(geo_root, bg='lightgreen', font='Colibri 10', text=f'Широта: {coordinates[0]}\nДолгота: {coordinates[1]}')
    coords_label.pack(pady=10)

def search(event):
    city = enter_city.get()
    wikipedia.set_lang('ru')
    try:
        wiki_info = wikipedia.summary(city)
        wiki_info_success(wiki_info)

    except:
        any_fail()

def geography_info(event):
    city = enter_city.get()
    try:
        geolocator = Nominatim(user_agent="http")
        location = geolocator.geocode(city)
        address = location.address
        coordinates = (location.latitude, location.longitude)
        geo_success(address, coordinates)

    except:
        any_fail()


def main_programm(event):
    global root_main

    city = enter_city.get()
    if city == '':
        open_main_programm()
    else:
        root_main = Toplevel(root)
        root_main.title(city)
        root_main.geometry('600x400+650+350')
        root_main.resizable(width=False, height=False)

        city_name_label = Label(root_main, bg='lightgreen', font='Colibri 10', text=f'Ваш город: {city}')
        city_name_label.pack(pady=5)

        city_info_label = Label(root_main, bg='lightgreen', font='Colibri 10', text=f'Выберите необходимую информацию')
        city_info_label.pack(pady=5)

        information = Button(root_main, bg='sky blue', font='Colibri 10', text='Краткая информация')
        information.pack(pady=5)
        information.bind('<Button-1>', search)

        geography = Button(root_main, bg='sky blue', font='Colibri 10', text='Координаты')
        geography.pack(pady=5)
        geography.bind('<Button-1>', geography_info)

        weather = Button(root_main, bg='sky blue', font='Colibri 10', text='Погода')
        weather.pack(pady=5)
        weather.bind('<Button-1>', weather_search)

        photos = Button(root_main, bg='sky blue', font='Colibri 10', text='Фото')
        photos.pack(pady=5)
        photos.bind('<Button-1>', show_photos)


def open_main_programm():
    global root_city
    root_city = Toplevel(root)
    root_city.title('Выбор города')
    root_city.geometry('600x400+650+350')
    root_city.resizable(width=False, height=False)

    city_label = Label(root_city, bg='sky blue', font='Colibri 10', text='Введите город: ')
    city_label.pack(pady=5)

    city_entry = Entry(root_city, textvariable=enter_city)
    city_entry.pack(pady=5)

    OK_button = Button(root_city, bg='yellow', font='Colibri 10', text='OK')
    OK_button.pack(pady=5)
    OK_button.bind('<Button-1>', main_programm)


def welcome():  # функция определяет время суток для вывода в приветствие
    currentTime = datetime.datetime.now()
    if currentTime.hour < 6:
        return 'Good night'
    if 6 <= currentTime.hour < 12:
        return 'Good morning'
    elif 12 <= currentTime.hour < 18:
        return 'Good afternoon'
    else:
        return 'Good evening'
def check_fetch_lgn(lgn):
    cursor.execute(f'SELECT login, password FROM users WHERE login = "{lgn}"')
    try:
        print(cursor.fetchone()[0])

        return True
    except:
        return False

def check_fetch_psw(lgn, psw):
    cursor.execute(f'SELECT login, password FROM users WHERE login = "{lgn}"')
    try:
        var = cursor.fetchone()[1]
        print(var)
        if psw == var:
            return True
        else:
            return False
    except:
        return False

def authorization(event):  # выполняется при нажатии ОК главного root
    lgn = login.get()  # забирает значение с ввода в Entry()
    psw = password1.get()
    print(lgn)
    print(psw)

    cursor.execute(f'SELECT login, password FROM users WHERE login = "{lgn}"')
    if lgn == '' and psw == '':
        messagebox.showwarning('Авторизация', 'Данные не введены')
    elif lgn != '' and psw == '':
        messagebox.showwarning('Авторизация', 'Пароль не введен')
    elif lgn != '' and psw != '' and check_fetch_lgn(lgn) is False:
        messagebox.showwarning('Авторизация', 'Пользователя не существует')
    elif check_fetch_lgn(lgn) is True and check_fetch_psw(lgn, psw) is False:
        messagebox.showwarning('Авторизация', 'Неверный пароль')
    else:
        open_main_programm()
def registration_failed(text):
    root4 = Toplevel(root2)
    root4.title('Ошибка регистрации')
    root4.geometry('800x100+550+450')
    root4.resizable(width=False, height=False)

    fail_label = Label(root4, bg='sky blue', font='Colibri 10', text=text)
    fail_label.pack(pady=35)


def registr(event):  # это работает!!! Получаем значение из Entry регистрации и подаем его в базу данных
    registr_get = registr1.get()
    new_password = password_reg.get()

    def legit_password(new_password, registr_get):
        if psw_check.check_len(new_password) == False:
            registration_failed('Длина пароля должная быть от 12 до 16 символов')
        elif psw_check.check_numbers(new_password) == False:
            registration_failed('В пароле должна быть минимум одна цифра')
        elif psw_check.check_upper_lower(new_password) == False:
            registration_failed('В пароле дожна быть минимум одна заглавная и одна строчная буква')
        elif psw_check.check_other_symbols(new_password) == False:
            registration_failed(
                'Пароль может содержать только заглавные и строчные буквы латинского алфавита, цифры и знак нижнего подчеркивания')
        elif all([psw_check.check_len(new_password), psw_check.check_numbers(new_password),
                  psw_check.check_upper_lower(new_password), psw_check.check_other_symbols(new_password)]):

            cursor.execute(f'SELECT login, password FROM users WHERE login = "{registr_get}"')
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO users VALUES (?, ?)', (registr_get, new_password))
                database.commit()
                print('aaa')

    legit_password(new_password, registr_get)
    # print(registr_get, new_password)


def registration(event):  # выполняется при нажатии Регистрация в главном root
    global root2
    root2 = Toplevel(root)  # синтаксии нового окна
    root2.title('Регистрация')
    root2.geometry('400x200+750+400')
    root2.resizable(width=False, height=False)

    registration_label_login = Label(root2, bg='sky blue', font='Colibri 10', text='Введите свой Login')
    registration_label_login.pack(pady=5)

    new_login = Entry(root2, textvariable=registr1)
    new_login.pack(pady=5)

    registration_label_password = Label(root2, bg='sky blue', font='Colibri 10', text='Введите свой пароль')
    registration_label_password.pack(pady=5)

    new_password = Entry(root2, textvariable=password_reg)
    new_password.pack(pady=5)

    registration_button = Button(root2, bg='yellow', font='Colibri 10', text='Регистрация')
    registration_button.pack(pady=5)
    registration_button.bind('<Button-1>', registr)


welcome_label = Label(root, font='Colibri 10', text=f'{welcome()}, user!', relief='flat')
welcome_label.pack(pady=(5, 0))

login_label = Label(root, bg='sky blue', font='Colibri 10', text='Login')
login_label.pack(pady=(5, 5))

login = Entry(textvariable=login)
login.pack(pady=5)

password_label = Label(root, bg='sky blue', font='Colibri 10', text='Password')
password_label.pack(pady=5)

password = Entry(textvariable=password1)
password.pack(pady=5)

OK_button = Button(root, bg='yellow', font='Colibri 10', text='OK')  # кнопка OK главного root
OK_button.pack(pady=5)
OK_button.bind('<Button-1>', authorization)  # <Button-1> - левая кнопка мыши test - функция выполнения

registry = Button(root, bg='lightgreen', font='Colibri 10', text='Регистрация')  # кнопка Регистрация главного root
registry.pack(pady=5)
registry.bind('<Button-1>', registration)

root.mainloop()
