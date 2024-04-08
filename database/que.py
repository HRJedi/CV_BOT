# This Python file uses the following encoding: utf-8


# Проверить наличие пользователя в БД
init_user_q = '''SELECT
                    COUNT(user_id)
                FROM
                    "CV_BOT".users
                WHERE
                    user_id = %s;'''


# Добавить нового пользователя
new_user_q = '''INSERT INTO "CV_BOT".users
                    (user_id, f_name_tg, l_name_tg, username)
                VALUES
                    (%s, %s, %s, %s);'''


# Получить текущий стейт пользователя
get_state_q = '''SELECT
                    state
                FROM
                    "CV_BOT".u_state
                WHERE
                    user_id = %s;'''


# Обновить список "Факты о себе"
set_about_q = '''INSERT INTO "CV_BOT".u_bot_interact
                    (user_id, upd_date ,fl_state)
                VALUES
                    (%s, now(), %s)
                ON CONFLICT
                    (user_id)
                DO UPDATE SET
                    upd_date = EXCLUDED.upd_date,
                    fl_state = EXCLUDED.fl_state;'''


# Получить кол-во элементов в списке "Факты о себе"
get_len_q = '''SELECT
                *
            FROM
                "CV_BOT".get_len_flist(%s);'''


# Получить случайный факт
get_r_fact_q = '''SELECT
                    *
                FROM
                    "CV_BOT".get_rand_fact(%s);'''


# Изменить текущий стейт пользователя
set_state_q = '''INSERT INTO "CV_BOT".u_state
                    (user_id, upd_date, state, addition, user_message)
                VALUES
                    (%s, now(), %s, %s, %s)
                ON CONFLICT
                    (user_id)
                DO UPDATE SET
                    user_id = EXCLUDED.user_id,
                    upd_date = EXCLUDED.upd_date,
                    state = EXCLUDED.state,
                    addition = EXCLUDED.addition,
                    user_message = EXCLUDED.user_message;'''

# Логировать действие без изменения стейта
new_log_q = '''INSERT INTO "CV_BOT".u_log
                    (user_id, state, addition, user_message)
                VALUES
                    (%s, %s, %s, %s);'''
