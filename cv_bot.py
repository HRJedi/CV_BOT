# This Python file uses the following encoding: utf-8

import telebot
from database import con_db, que
from mod import mod
from content import keys, cont


# Перс. данные
token = "token"
forward_to = 'user'

# Бот
bot = telebot.TeleBot(token, num_threads=10)

# Вызовы всплывающих сообщений
alert_list = ['discl_m', 'fwd_about', 'src_about']

# Общие текстовые команды выхода
return_list = ['↩️ К началу', '↩️ К карьере', '↩️ К опыту работы']


# Запуск бота
@bot.message_handler(commands=['start'])
# Регистрация нового пользователя
def init(message):
    mod.new_user_reg(message)
    start(message)

    return


# Стартовое меню
def start(message):
    con_db.set_val(que.set_state_q,
                   (message.chat.id,
                    'Старт',
                    'ordinary',
                    message.text))
    bot.send_sticker(message.chat.id,
                     cont.sticker_my)
    bot.send_message(message.chat.id,
                     cont.start_mesage,
                     reply_markup=keys.start_m)

    return


# РАЗДЕЛЫ
#
# Раздел о карьере
@bot.callback_query_handler(func=lambda call:
                            call.data == 'career_m')
def career_m(call):
    con_db.set_val(que.set_state_q,
                   (call.message.chat.id,
                    'О карьере',
                    'ordinary',
                    'NULL'))
    bot.send_message(call.message.chat.id,
                     cont.career_text,
                     reply_markup=keys.career_m)

    return


# Раздел контактов
@bot.callback_query_handler(func=lambda call:
                            call.data == 'cont_m')
def cont_m(call):
    con_db.set_val(que.new_log_q,
                   (call.message.chat.id,
                    'Контакты',
                    'ordinary',
                    'NULL'))
    bot.send_message(call.message.chat.id,
                     cont.cont_text,
                     reply_markup=keys.cont_m_inl)
    bot.send_contact(call.message.chat.id,
                     '79050207805',
                     'Кирилов',
                     'Павел',
                     reply_markup=keys.cont_m)

    return


# Раздел пересылки сообщений
@bot.callback_query_handler(func=lambda call:
                            call.data == 'fwd_m')
def fwd_m(call):
    con_db.set_val(que.set_state_q,
                   (call.message.chat.id,
                    'Пересылка',
                    'ordinary',
                    'NULL'))
    bot.send_message(call.message.chat.id,
                     cont.msg_text,
                     reply_markup=keys.fwd_m)

    return


# Раздел о боте
@bot.callback_query_handler(func=lambda call:
                            call.data == 'about_bot')
def about_b(call):
    con_db.set_val(que.new_log_q,
                   (call.message.chat.id,
                    'О боте',
                    'ordinary',
                    'NULL'))
    bot.send_message(call.message.chat.id,
                     cont.ab_bot_text,
                     reply_markup=keys.ab_bot_m)

    return


# СКВОЗНЫЕ ОБРАБОТЧИКИ
#
# Общий обработчик для всплывающих сообщений
@bot.callback_query_handler(func=lambda call:
                            call.data in alert_list)
def alerts(call):

    if call.data == 'discl_m':
        con_db.set_val(que.new_log_q,
                       (call.message.chat.id,
                        'Дисклеймер',
                        'pop-up message',
                        'NULL'))
        bot.answer_callback_query(call.id,
                                  show_alert=True,
                                  text=cont.discl)

    elif call.data == 'fwd_about':
        con_db.set_val(que.new_log_q,
                       (call.message.chat.id,
                        'Справка: режим пересылки',
                        'pop-up message',
                        'NULL'))
        bot.answer_callback_query(call.id,
                                  show_alert=True,
                                  text=cont.fwd_ab)

    elif call.data == 'src_about':
        con_db.set_val(que.new_log_q,
                       (call.message.chat.id,
                        'Справка: вкраце',
                        'pop-up message',
                        'NULL'))
        bot.answer_callback_query(call.id,
                                  show_alert=True,
                                  text=cont.src_ab)

    return


# Общий обработчики текстовых команд выхода
@bot.message_handler(func=lambda message:
                     message.text in return_list,
                     content_types=['text'])
def common_return(message):

    if message.text == '↩️ К началу':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Старт',
                        'return_to_prew',
                        message.text))
        bot.send_message(message.chat.id,
                         mod.act_state_msg(message),
                         reply_markup=keys.hidekey)
        bot.send_message(message.chat.id,
                         '↩️',
                         reply_markup=keys.hidekey)
        start(message)

    elif message.text == '↩️ К карьере':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'О карьере',
                        'return_to_prew',
                        message.text))
        bot.send_message(message.chat.id,
                         '↩️',
                         reply_markup=keys.career_m)

    elif message.text == '↩️ К опыту работы':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы',
                        'return_to_prew',
                        message.text))
        bot.send_message(message.chat.id,
                         '↩️',
                         reply_markup=keys.exp_m)

    return


# МЕНЮ L2
#
# О карьере - меню
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'О карьере',
                     content_types=['text'])
def career_messages(message):

    # Вкраце - меню
    if message.text == '👤 Вкраце':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Вкраце',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.about_text,
                         reply_markup=keys.about_m)
        mod.cv_message_set(bot, message)
        bot.send_message(message.from_user.id,
                         cont.alarm_pin,
                         reply_markup=keys.src_alert_m)

    # Опыт работы - меню
    elif message.text == '🗓 Опыт работы':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.exp_text,
                         reply_markup=keys.exp_m)

    # Образование - меню
    elif message.text == '🎓 Образование':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Образование',
                        'ordinary',
                        message.text))
        bot.send_sticker(message.chat.id,
                         cont.sticker_kpfu)
        bot.send_message(message.from_user.id,
                         cont.edu_text,
                         reply_markup=keys.edu_m)

    # Hardskills - меню
    elif message.text == '👨🏻‍💻 Hard Skills':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Hard Skills',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.hs_text,
                         reply_markup=keys.hs_m)

    # Слабые стороны - меню
    elif message.text in ['⛔️ Слабые стороны', '⛔️ Недостатки']:
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Слабые стороны',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.weak_s_text,
                         reply_markup=keys.weak_s_m)

    # Сильные стороны - меню
    elif message.text in ['✅ Сильные стороны', '✅ Достоинства']:
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Сильные стороны',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.strong_s_text,
                         reply_markup=keys.strong_s_m)

    # Резюме - меню
    elif message.text == '📄 Резюме':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Резюме',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.cv_text,
                         reply_markup=keys.cv_m)
        bot.send_message(message.from_user.id,
                         cont.cv_text1,
                         reply_markup=keys.dyn_keys(['📋 HH.RU', mod.cv_hh]))
        bot.send_document(message.chat.id,
                          open(r'/root/CV_BOT/' + cont.cv_path, 'rb'))

    # Карьерный трек - меню
    elif message.text == '📈 Карьерный трек':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Карьерный трек',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.career_track_text,
                         reply_markup=keys.career_track_m)

    # Случайный факт - меню
    elif message.text == '🎲 О себе':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'О себе',
                        'ordinary',
                        message.text))
        bot.send_message(message.from_user.id,
                         cont.rand_fact_text,
                         reply_markup=keys.r_fact_m2)

    return


# Пересылка сообщений - меню
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Пересылка',
                     content_types=['text'])
def fwd_mesages(message):
    con_db.set_val(que.new_log_q,
                   (message.chat.id,
                    'Пересылка',
                    'new_fwd_message',
                    message.text))
    bot.send_message(message.chat.id,
                     'Ваше сообщение отправлено 👌🏻',
                     reply_markup=keys.fwd_alert_m)
    bot.forward_message(forward_to,
                        message.chat.id,
                        message.message_id)

    return


# МЕНЮ L3
#
# Случайный факт - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'О себе',
                     content_types=['text'])
def r_fact_messages(message):

    if message.text == '🔄 Начать!':
        mod.upd_facts_func(message)
        mod.r_fact_func(bot, message)

    elif con_db.get_val(que.get_len_q,
                        (message.from_user.id,))[0] == 0:
        bot.send_message(message.from_user.id,
                         cont.facts_empty_text,
                         reply_markup=keys.r_fact_m1)

    elif message.text == '🎲 Факт!':
        mod.r_fact_func(bot, message)

    return


# Опыт работы - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Опыт работы',
                     content_types=['text'])
def exp_messages(message):

    if message.text == '👨🏻‍🎓 КФУ':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы: кфу',
                        'ordinary',
                        message.text))
        bot.send_sticker(message.chat.id,
                         cont.sticker_kpfu)
        bot.send_message(message.chat.id,
                         cont.kpfu_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '📚 Первый опыт':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы: первый опыт',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.f_exp_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🎓 ООО "Инновация"':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы: инновация',
                        'ordinary',
                        message.text))
        bot.send_sticker(message.chat.id,
                         cont.sticker_99)
        bot.send_message(message.chat.id,
                         cont.innov_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🚚  Альфаскан / Delko':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы: альфа/делко',
                        'ordinary',
                        message.text))
        bot.send_sticker(message.chat.id,
                         cont.sticker_alpha)
        bot.send_message(message.chat.id,
                         cont.alpha_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🥩 Мираторг':
        con_db.set_val(que.set_state_q,
                       (message.chat.id,
                        'Опыт работы: мираторг',
                        'ordinary',
                        message.text))
        bot.send_sticker(message.chat.id,
                         cont.sticker_mira)
        bot.send_message(message.chat.id,
                         cont.mira_text,
                         reply_markup=keys.exp_l3_m)

    return


# Образование - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Образование',
                     content_types=['text'])
def edu_messages(message):

    if message.text == '📈 Курсы':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Образование: курсы',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.cours_text,
                         reply_markup=keys.edu_m1)

    return


# Hard Skills - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Hard Skills',
                     content_types=['text'])
def hs_messages(message):

    if message.text == '🐍 Python':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Hard Skills: python',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.hs_python_text,
                         reply_markup=keys.hs_m)

    elif message.text == '🗄 SQL':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Hard Skills: sql',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.hs_sql_text,
                         reply_markup=keys.hs_m)

    elif message.text == '🧮 Excel':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Hard Skills: excel',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.hs_excel_text,
                         reply_markup=keys.hs_m)

    elif message.text == '👨‍🔬 Прикладное':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Hard Skills: прикладной софт',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.hs_special_text,
                         reply_markup=keys.hs_m)

    elif message.text == '⚙️ Процессы':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Hard Skills: процессы',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.hs_process_text,
                         reply_markup=keys.hs_m)

    elif message.text == '📊 BI':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Hard Skills: bi',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.hs_bi_text,
                         reply_markup=keys.hs_m)

    return


# МЕНЮ L4
#
# Опыт работы - первый опыт - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Опыт работы: кфу',
                     content_types=['text'])
def exp_kpfu_messages(message):

    if message.text == '📌 Задачи':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: кфу - задачи',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.kpfu_resp_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🏆 Достижения':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: кфу - достижения',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.kpfu_ach_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '⛔️ Увольнение':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: кфу - увольнение',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.kpfu_dism_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '👍🏻 Рекомендации':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: кфу - рекомендации',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.kpfu_rec_text,
                         reply_markup=keys.exp_l3_m)

    return


# Опыт работы - первый опыт - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Опыт работы: первый опыт',
                     content_types=['text'])
def exp_f_exp_messages(message):

    if message.text == '📌 Задачи':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: первый опыт - задачи',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.f_exp_resp_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🏆 Достижения':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: первый опыт - достижения',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.f_exp_ach_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '⛔️ Увольнение':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: первый опыт - увольнение',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.f_exp_dism_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '👍🏻 Рекомендации':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: первый опыт - рекомендации',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.f_exp_rec_text,
                         reply_markup=keys.exp_l3_m)

    return


# Опыт работы - Инновация - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Опыт работы: инновация',
                     content_types=['text'])
def exp_innov_messages(message):

    if message.text == '📌 Задачи':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: инновация - задачи',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.innov_resp_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🏆 Достижения':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: инновация - достижения',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.innov_ach_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '⛔️ Увольнение':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: инновация - увольнение',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.innov_dism_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '👍🏻 Рекомендации':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: инновация - рекомендации',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.innov_rec_text,
                         reply_markup=keys.exp_l3_m)

    return


# Опыт работы - Альфа - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Опыт работы: альфа/делко',
                     content_types=['text'])
def exp_alpha_messages(message):

    if message.text == '📌 Задачи':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: альфа/делко - задачи',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.alpha_resp_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🏆 Достижения':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: альфа/делко - достижения',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.alpha_ach_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '⛔️ Увольнение':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: альфа/делко - увольнение',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.alpha_dism_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '👍🏻 Рекомендации':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: альфа/делко - рекомендации',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.alpha_rec_text,
                         reply_markup=keys.exp_l3_m)

    return


# Опыт работы - Мираторг - подменю
@bot.message_handler(func=lambda message:
                     mod.act_state_msg(message) == 'Опыт работы: мираторг',
                     content_types=['text'])
def exp_mira_messages(message):

    if message.text == '📌 Задачи':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: мираторг - задачи',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.mira_resp_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '🏆 Достижения':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: мираторг - достижения',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.mira_ach_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '⛔️ Увольнение':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: мираторг - увольнение',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.mira_dism_text,
                         reply_markup=keys.exp_l3_m)

    elif message.text == '👍🏻 Рекомендации':
        con_db.set_val(que.new_log_q,
                       (message.chat.id,
                        'Опыт работы: мираторг - рекомендации',
                        'ordinary',
                        message.text))
        bot.send_message(message.chat.id,
                         cont.mira_rec_text,
                         reply_markup=keys.exp_l3_m)

    return


# Обращение к серверу
bot.polling(none_stop=True)
