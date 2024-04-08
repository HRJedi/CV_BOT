/* 
 * ТАБЛИЦЫ
 * */


CREATE TYPE "CV_BOT".user_stat AS ENUM ('active', 'inactive', 'for delete');
CREATE TABLE users
	("user_id" bigint PRIMARY KEY,
	"reg_date" timestamp NOT NULL DEFAULT now(),
	"f_name_tg" VARCHAR(50),
	"l_name_tg" VARCHAR(50),
	"username" VARCHAR(50),
	"f_name_real" VARCHAR(50),
	"l_name_real" VARCHAR(50),
	"tel_num" VARCHAR(50),
	"email" VARCHAR(100),
	"status" user_stat NOT NULL DEFAULT 'active');
	

CREATE TABLE "CV_BOT".u_state
	("user_id" bigint PRIMARY KEY,
	"upd_date" timestamp NOT NULL DEFAULT now(),
	"state" VARCHAR(50) NOT NULL DEFAULT 'Инициализация',
	"addition" VARCHAR(50) NOT NULL DEFAULT 'ordinary',
	"user_message" TEXT);


CREATE TABLE "CV_BOT".u_log
	("log_id" serial PRIMARY KEY,
	"event_date" timestamp NOT NULL DEFAULT now(),
	"user_id" bigint NOT NULL,
	"state" VARCHAR(50) NOT NULL DEFAULT 'Старт',
	"addition" VARCHAR(50) NOT NULL DEFAULT 'ordinary',
	"user_message" TEXT);


CREATE TABLE "CV_BOT".u_bot_interact
	("user_id" bigint PRIMARY KEY,
	"upd_date" timestamp NOT NULL DEFAULT now(),
	"fl_state" jsonb);


/* 
 * СТРУКТУРА
 * */


ALTER TABLE "CV_BOT".u_state
ADD CONSTRAINT fk_state_users
	FOREIGN KEY
	(user_id) REFERENCES "CV_BOT".users(user_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE;


ALTER TABLE "CV_BOT".u_log
ADD CONSTRAINT fk_log_users
	FOREIGN KEY
	(user_id) REFERENCES "CV_BOT".users(user_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE;

ALTER TABLE "CV_BOT".u_bot_interact
ADD CONSTRAINT fk_interact_users
	FOREIGN KEY
	(user_id) REFERENCES "CV_BOT".users(user_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE;
	

/* 
 * ТРИГГЕРЫ
 * */


/* Добавить стейт после инициализации */
CREATE OR REPLACE FUNCTION user_insert_trigger_fnc()
RETURNS trigger AS
$$
BEGIN
INSERT INTO "CV_BOT".u_state
	(user_id, upd_date, state, addition, user_message)
VALUES
	(NEW.user_id, now(), DEFAULT, DEFAULT, NULL)
ON CONFLICT
	(user_id)
DO UPDATE SET
	upd_date = EXCLUDED.upd_date,
	state = EXCLUDED.addition,
	addition = 'conlfict',
	user_message = EXCLUDED.user_message;
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER 
	user_insert_trigger
AFTER INSERT
ON 
	"CV_BOT".users
FOR EACH ROW
EXECUTE PROCEDURE 
	user_insert_trigger_fnc();


/* Добавить лог после смены стейта */
CREATE OR REPLACE FUNCTION new_state_trigger_fnc()
RETURNS trigger AS
$$
BEGIN
INSERT INTO "CV_BOT".u_log
	(user_id, state, addition, user_message)
VALUES
	(NEW.user_id, NEW.state, NEW.addition, NEW.user_message);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER 
	new_state_trigger
AFTER INSERT OR UPDATE
ON 
	"CV_BOT".u_state
FOR EACH ROW
EXECUTE PROCEDURE 
	new_state_trigger_fnc();


/* Получить случайный факт и удалить его из актуального списка */
CREATE OR REPLACE FUNCTION "CV_BOT".get_rand_fact (id bigint) RETURNS text AS $$
DECLARE
	elem integer;
	fact TEXT;
BEGIN
	SELECT
		floor(jsonb_array_length(fl_state) * random())::int
	INTO elem
	FROM
		"CV_BOT".u_bot_interact ui
	WHERE
		user_id = id;
	SELECT
		Concat(fl_state -> elem ->> 'text', ';', fl_state -> elem ->> 'item')
	INTO fact
	FROM
		"CV_BOT".u_bot_interact ui1
	WHERE
		user_id = id;
	UPDATE 
		"CV_BOT".u_bot_interact 
	SET 
		fl_state = fl_state - elem
  	WHERE 
  		user_id = id;
  	RETURN
  		fact;
END;
$$ LANGUAGE plpgsql;


/* Получить кол-во элементов в списке фактов */
CREATE OR REPLACE FUNCTION "CV_BOT".get_len_flist (id bigint) RETURNS int AS $$
DECLARE
	len integer;
BEGIN
	SELECT
		jsonb_array_length(fl_state)::int
	INTO len
	FROM
		"CV_BOT".u_bot_interact ui
	WHERE
		user_id = id;
  	RETURN
  		len;
END;
$$ LANGUAGE plpgsql;


/*

DROP FUNCTION IF EXISTS get_len_flist(numeric);
DROP FUNCTION IF EXISTS get_rand_fact(numeric);
DROP TRIGGER IF EXISTS new_state_trigger ON "CV_BOT".users_state;
DROP TRIGGER IF EXISTS user_insert_trigger ON "CV_BOT".users;

*/