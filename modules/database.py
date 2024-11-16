import psycopg2  # для работы с PostgreSQL
from config import ConfigBotClass
from psycopg2 import pool


# Создаем пул соединений
try:
    postgresql_pool = psycopg2.pool.SimpleConnectionPool(
        2, 5,
        dsn=ConfigBotClass.URL_DATABASE
    )
    if postgresql_pool:
        print("Пул соединений создан успешно")
except (Exception, psycopg2.DatabaseError) as error:
    print ("Ошибка при подключении к PostgreSQL", error)
    postgresql_pool = None  # Устанавливаем пул в None в случае ошибки


def add_user_to_db(telegram_id):
    try:
        # Получаем соединение из пула
        conn = postgresql_pool.getconn()
        if conn:
            cursor = conn.cursor()

            # Проверка, существует ли пользователь в базе
            cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
            user = cursor.fetchone()

            if user is None:
                # Если пользователя нет в базе, добавляем нового с 5 кредитами
                cursor.execute('INSERT INTO users (telegram_id, user_balance) VALUES (%s, %s)',
                               (telegram_id, ConfigBotClass.START_USER_BALANCE))
                conn.commit()
                print(f"Пользователь с ID {telegram_id} успешно добавлен в базу данных.")
                return True  # Новый пользователь добавлен
            else:
                # Если пользователь уже существует, ничего не делаем
                return False

        else:
            print("Не удалось получить соединение из пула")
            return False
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False
    finally:
        if conn:
            cursor.close()
            postgresql_pool.putconn(conn)  # Возвращаем соединение в пул


def show_users_table():
    # Получаем соединение из пула
    conn = postgresql_pool.getconn()

    if conn:
        try:
            # Создаем курсор
            cursor = conn.cursor()

            # Выполняем запрос
            cursor.execute("SELECT * FROM users;")

            # Получаем все строки из результата запроса
            show_users = cursor.fetchall()

            # Возвращаем данные
            return show_users

        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
        finally:
            # Возвращаем соединение в пул
            postgresql_pool.putconn(conn)

    else:
        print("Не удалось получить соединение из пула.")
        return None

# # Функция для создания таблицы users
# def create_users_table():
#     if not postgresql_pool:
#         print("Пул соединений не создан, не могу продолжить.")
#         return
#
#     try:
#         # Получаем соединение из пула
#         conn = postgresql_pool.getconn()
#
#         with conn.cursor() as cursor:
#             # Создаем таблицу (если она не существует)
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS users (
#                     telegram_id BIGINT PRIMARY KEY,
#                     user_balance DECIMAL DEFAULT 0,
#                     registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 );
#             """)
#             conn.commit()
#             print("Таблица users успешно создана (или уже существует).")
#     except Exception as e:
#         print(f"Ошибка при создании таблицы: {e}")
#     finally:
#         # Возвращаем соединение в пул
#         if conn:
#             postgresql_pool.putconn(conn)



# # Функция для подключения к базе данных
# def get_db_connection():
#     try:
#         connection = psycopg2.connect(ConfigBotClass.URL_DATABASE)
#         print("Подключение успешно!")
#         return connection
#     except Exception as e:
#         print(f"Ошибка при подключении к базе данных: {e}")
#         return None