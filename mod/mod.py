# This Python file uses the following encoding: utf-8


import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from database import con_db, que
from content import keys, cont

cv_hh = 'cv'
geo_token = 'token'


# ФУНКЦИИ БД
# Новый пользователь
def new_user_reg(message):

    if con_db.get_val(que.init_user_q,
                      (message.chat.id,))[0] == 0:
        uid = message.chat.id
        f_name = message.from_user.first_name
        l_name = message.from_user.last_name
        u_name = message.from_user.username
        con_db.set_val(que.new_user_q,
                       (uid,
                        f_name,
                        l_name,
                        u_name))
        con_db.set_val(que.set_about_q,
                       (uid,
                        cont.about_me))
    return


# Получить актуальный стейт юзера для сообщений
def act_state_msg(message):
    state = con_db.get_val(que.get_state_q,
                           (message.chat.id,))
    return state[0]

# Получить актуальный стейт юзера для вызова


def act_state_call(call):
    state = con_db.get_val(que.get_state_q,
                           (call.message.chat.id,))[0]
    return state


# Обновить список фактов
def upd_facts_func(message):
    con_db.set_val(que.set_about_q,
                   (message.chat.id,
                    cont.about_me))
    con_db.set_val(que.new_log_q,
                   (message.chat.id,
                    'О себе',
                    'refresh_fact_list',
                    message.text))
    return


# Выдача случайного факта
def r_fact_func(bot, message):
    bot.send_dice(message.chat.id,
                  '🎲')
    res = con_db.get_val(que.get_r_fact_q,
                         (message.from_user.id,))[0].split(';')
    con_db.set_val(que.new_log_q,
                   (message.chat.id,
                    'О себе',
                    'send_random_fact',
                    message.text))
    bot.send_message(message.from_user.id,
                     res[0],
                     reply_markup=keys.r_fact_m2)

    if len(res[1]) > 2:
        bot.send_photo(message.chat.id,
                       open(r'/root/CV_BOT/pic/' + res[1], 'rb'))
    return


# Получить координаты города
def get_geo(city_name):
    token = geo_token
    # Поиск по городам в евразии, вернуть json
    loc = requests.get(
        f'https://eu1.locationiq.com/v1/search?key={token}&q={city_name}&format=json&').json()
    return {'lat': loc[0]['lat'], 'lon': loc[0]['lon']}


# Парсинг резюме + геопозиция
def get_cv():
    cv_link = cv_hh
    uClient = uReq(cv_link)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, features='html.parser')

    # Название резюме
    container = page_soup.find_all(
        'div', {'class': 'resume-block__title-text-wrapper'})[0]
    cv_name = container.find('span', class_='resume-block__title-text').text

    # Образование
    container = page_soup.find_all('div', {
                                   'data-qa': 'resume-block-education'})[0]
    e_uni = container.find('div', class_='bloko-text bloko-text_strong').text
    e_dep = container.find(
        'div', {'data-qa': 'resume-block-education-organization'}).text.split(', ')[0]

    # Стаж
    container = page_soup.find_all('span', {
                                   'class': 'resume-block__title-text resume-block__title-text_sub'})[0]
    e_exp = container.text.replace('Опыт работы ', '')

    # Основная информация (Общая)
    container = page_soup.find_all('div', {'class': 'resume-header-main'})[0]

    # Релок и коммандировки
    temp_lst = []
    e_loc = container.find('div', {'class': 'resume-header-title'})
    for part in e_loc:
        if part is not None:
            temp_lst.append(part.text)
    temp_lst = temp_lst[-1]
    reloc = temp_lst.split(", ")[-2]
    r_trip = temp_lst.split(", ")[-1]

    # Ссылка на фото в резюме
    e_photo = container.find('img', {'class': 'resume-media__image'})['src']

    # Имя
    e_name = container.find('h2', class_='bloko-header-1').text

    # Возраст
    e_age = container.find('span', {'data-qa': 'resume-personal-age'}).text

    # Город
    e_city = container.find('span', {'data-qa': 'resume-personal-address'}).text

    # Контакты
    temp_lst = []
    for part in container.find('div', class_='resume-header-field'):
        if part.find('a', class_='bloko-link') is not None:
            for elem in part:
                temp_lst.append(elem.text.split('\xa0'))
    tel_num = temp_lst[2][1]
    e_mail = temp_lst[3][0]
    tg_link = temp_lst[4][0]

    atr_list = {'название': cv_name, 'фото': e_photo, 'фио': e_name,
                'возраст': e_age, 'стаж': e_exp, 'город': e_city,
                'универ': e_uni, 'кафедра': e_dep, 'релок': reloc,
                'команд': r_trip, 'телефон': tel_num, 'почта': e_mail,
                'ссылка': tg_link, 'коорд': get_geo(e_city)}

    return atr_list


def cv_message_set(bot, message):
    cv_dict = get_cv()
    bot.send_photo(message.chat.id,
                   cv_dict["фото"])
    bot.send_message(message.from_user.id,
                     (f'👤 - Общая информация:\n'
                      f'{cv_dict["фио"]}\n'
                      f'{cv_dict["возраст"]}\n\n'
                      f'👨🏻‍💻 - Позиция: \n'
                      f'{cv_dict["название"]}\n'
                      f'{cv_dict["стаж"]}\n\n'
                      f'🎓 - Образование:\n'
                      f'{cv_dict["универ"]}\n'
                      f'{cv_dict["кафедра"]}\n\n'
                      f'📍 - Локация:\n'
                      f'{cv_dict["город"]}\n'
                      f'{cv_dict["релок"]}\n'
                      f'{cv_dict["команд"]}'),
                     reply_markup=keys.about_m)

    bot.send_contact(message.chat.id,
                     cv_dict['телефон'],
                     cv_dict['фио'].split(' ')[1],
                     cv_dict['фио'].split(' ')[0])

    bot.send_location(message.chat.id,
                      longitude=cv_dict['коорд']['lon'],
                      latitude=cv_dict['коорд']['lat'],
                      horizontal_accuracy=1000)
    return
