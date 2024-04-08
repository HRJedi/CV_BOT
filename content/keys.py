# This Python file uses the following encoding: utf-8

from telebot import types as t

# Комманды
hidekey = t.ReplyKeyboardRemove()


# Dynamic Inline Markups
# Принимает на вход список - url и текст
def dyn_keys(lst):
    markup = t.InlineKeyboardMarkup(row_width=1)
    b = t.InlineKeyboardButton(text=lst[0],
                               url=lst[1])
    markup.add(b)
    return markup

# Keys


# Кнопки - Общие
to_start_b = t.KeyboardButton('↩️ К началу')
to_car_b = t.KeyboardButton('↩️ К карьере')
to_exp_b = t.KeyboardButton('↩️ К опыту работы')


# Кнопки - О карьере
about_b = t.KeyboardButton('👤 Вкраце')
exp_b = t.KeyboardButton('🗓 Опыт работы')
ed_b = t.KeyboardButton('🎓 Образование')
hs_b = t.KeyboardButton('👨🏻‍💻 Hard Skills')
weak_b = t.KeyboardButton('⛔️ Слабые стороны')
strng_b = t.KeyboardButton('✅ Сильные стороны')
cv_b = t.KeyboardButton('📄 Резюме')
c_track_b = t.KeyboardButton('📈 Карьерный трек')
facts_b = t.KeyboardButton('🎲 О себе')

# Кнопки - Режим пересылки
res_fact_b = t.KeyboardButton('🔄 Начать!')
new_fact_b = t.KeyboardButton('🎲 Факт!')

# Кнопки - Опыт работы
kpfu_b = t.KeyboardButton('👨🏻‍🎓 КФУ')
f_exp_b = t.KeyboardButton('📚 Первый опыт')
innov_b = t.KeyboardButton('🎓 ООО "Инновация"')
alpha_b = t.KeyboardButton('🚚  Альфаскан / Delko')
mira_b = t.KeyboardButton('🥩 Мираторг')

# Кнопки - образование
edu_cours_b = t.KeyboardButton('📈 Курсы')

# Кнопки - Hard Skills
hs_python_b = t.KeyboardButton('🐍 Python')
hs_sql_b = t.KeyboardButton('🗄 SQL')
hs_excel_b = t.KeyboardButton('🧮 Excel')
hs_special_b = t.KeyboardButton('👨‍🔬 Прикладное')
hs_process_b = t.KeyboardButton('⚙️ Процессы')
hs_bi_b = t.KeyboardButton('📊 BI')

# Кнопки - Слабые стороны
redir_weak_b = t.KeyboardButton('⛔️ Недостатки')

# Кнопки - Слабые стороны
redir_strong_b = t.KeyboardButton('✅ Достоинства')

# Кнопки - Режим пересылки
res_fact_b = t.KeyboardButton('🔄 Начать!')

# Кнопки L3
#
# Опыт работы

# Кнопки подробности по местам работы
exp_resp_b = t.KeyboardButton('📌 Задачи')
exp_ach_b = t.KeyboardButton('🏆 Достижения')
exp_dism_b = t.KeyboardButton('⛔️ Увольнение')
exp_rec_b = t.KeyboardButton('👍🏻 Рекомендации')


# Markups

# Меню - О боте
ab_bot_m = t.ReplyKeyboardMarkup(resize_keyboard=True)
ab_bot_m.add(to_start_b)

# Меню - О карьере
career_m = t.ReplyKeyboardMarkup(row_width=2)
career_m.add(about_b, exp_b, ed_b, hs_b, weak_b, strng_b,
             cv_b, c_track_b, facts_b, to_start_b)

# Меню - Вкраце
about_m = t.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
about_m. add(to_car_b)

# Меню - Контакты
cont_m = t.ReplyKeyboardMarkup(resize_keyboard=True)
cont_m.add(to_start_b)

# Меню - Режим пересылки
fwd_m = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
fwd_m.add(to_start_b)

# Меню1 - Случайный факт
r_fact_m1 = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
r_fact_m1.add(to_car_b, res_fact_b)

# Меню2 - Случайный факт
r_fact_m2 = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
r_fact_m2.add(to_car_b, new_fact_b)

# Меню - Опыт
exp_m = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
exp_m.add(kpfu_b, f_exp_b, innov_b, alpha_b, mira_b, to_car_b)

# Меню - Образование
edu_m = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
edu_m.add(edu_cours_b, to_car_b)

# Меню - Образование1
edu_m1 = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
edu_m1.add(to_car_b)

# Меню - hard skills
hs_m = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
hs_m.add(hs_python_b,
         hs_sql_b,
         hs_excel_b,
         hs_special_b,
         hs_process_b,
         hs_bi_b,
         to_car_b)

# Меню - слабые стороны
weak_s_m = t.ReplyKeyboardMarkup(resize_keyboard=True)
weak_s_m.add(redir_strong_b, to_car_b)

# Меню - сильные стороны
strong_s_m = t.ReplyKeyboardMarkup(resize_keyboard=True)
strong_s_m.add(redir_weak_b, to_car_b)

# Меню - Резюме
cv_m = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
cv_m.add(to_car_b)

# Меню - Карьерный трек
career_track_m = t.ReplyKeyboardMarkup(resize_keyboard=True)
career_track_m.add(to_car_b)

# МЕНЮ L3
#
# Меню опыт - Выпадающие меню
exp_l3_m = t.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
exp_l3_m.add(exp_resp_b, exp_ach_b, exp_dism_b, exp_rec_b, to_exp_b)


# Inline keys

# Кнопки - Старт
career_b = t.InlineKeyboardButton(text='💼 О карьере', callback_data='career_m')
cont_b = t.InlineKeyboardButton(text='📞 Связаться со мной', callback_data='cont_m')
fwd_m_b = t.InlineKeyboardButton(text='🤖 Написать через бота', callback_data='fwd_m')
about_b_m_b = t.InlineKeyboardButton(text='🔧 Подробнее о боте', callback_data='about_bot')
discl_b = t.InlineKeyboardButton(text='⚠️ Дисклеймер', callback_data='discl_m')


# Кнопки - Контакты
mail_b = t.InlineKeyboardButton(
    text='📧 Написать на почту',
    url='overmind.kirilov@gmail.com')
tg_b = t.InlineKeyboardButton(
    text='💬 Написать в TG',
    url='https://t.me/psy_kirilov')
wa_b = t.InlineKeyboardButton(
    text='💬 Написать в WA',
    url='https://wa.me/qr/IDOCD66LJ476K1')


# Inline Markups

# Меню - Старт
start_m = t.InlineKeyboardMarkup(row_width=1)
start_m.add(career_b, cont_b, fwd_m_b, about_b_m_b, discl_b)

# Меню - Контакты
cont_m_inl = t.InlineKeyboardMarkup(row_width=1)
cont_m_inl.add(tg_b, wa_b)


# Кнопки - alert list
src_about_b = t.InlineKeyboardButton(text='ℹ️ Источник', callback_data='src_about')
fwd_about_b = t.InlineKeyboardButton(text='ℹ️ О пересылке', callback_data='fwd_about')


# Меню - alert

# Алерт режима пересылки
fwd_alert_m = t.InlineKeyboardMarkup(row_width=1)
fwd_alert_m.add(fwd_about_b)

# Алерт раздела "вкраце"
src_alert_m = t.InlineKeyboardMarkup(row_width=1)
src_alert_m.add(src_about_b)
