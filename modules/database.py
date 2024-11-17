import psycopg2  # для работы с PostgreSQL
from config import ConfigBotClass
from psycopg2 import pool


# Создаем пул соединений
try:
    postgresql_pool = psycopg2.pool.SimpleConnectionPool(
        2, 3,
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


def get_number_of_users():
    """Функция для получения количества пользователей в базе данных."""
    conn = postgresql_pool.getconn()  # Получаем соединение из пула

    if not conn:
        print("Не удалось получить соединение из пула.")
        return 0  # Возвращаем 0, если соединение не удалось получить

    try:
        cursor = conn.cursor()  # Создаём курсор
        cursor.execute("SELECT COUNT(*) FROM users;")  # Запрос на получение количества пользователей
        result = cursor.fetchone()  # Получаем результат

        # Возвращаем количество пользователей
        return result[0] if result else 0

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return 0  # В случае ошибки возвращаем 0

    finally:
        postgresql_pool.putconn(conn)  # Возвращаем соединение в пул


def get_telegram_id_all_users():
    """Функция для получения telegram_id всех пользователей в базе данных."""
    conn = postgresql_pool.getconn()

    if not conn or conn.closed:
        print("Соединение закрыто или не удалось получить соединение из пула.")
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id FROM users;")
        result = cursor.fetchall()
        return result

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return []

    finally:
        postgresql_pool.putconn(conn)

