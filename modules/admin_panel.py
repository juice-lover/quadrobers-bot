import time
from datetime import datetime, timedelta

from modules import database, keyboard


# Функция обработки вызова админ панели
def send_admin_panel_to_admin(bot, message) :
    try:
        # Получаем количество пользователей из базы данных
        number_of_users = database.get_number_of_users()

        # Формируем сообщение для админа
        text_message = (f"Админ панель\n\n"
                        f"Количество пользователей: {number_of_users}")

        bot.reply_to(message, text_message, reply_markup=keyboard.create_inline_admin_buttons())

    except Exception as e:
        # Обработка возможных ошибок
        bot.reply_to(message, "Произошла ошибка при получении данных.")
        print(f"Ошибка в админ панели: {e}")


def send_msg_all_users_function(bot, message):
    """Функция для рассылки сообщений всем пользователям с уведомлением администратора."""

    # Проверяем текст сообщения
    if message.text == "Отменить операцию":
        bot.reply_to(message, "✅ Операция успешно отменена!")
        return

    # Получаем список telegram_id всех пользователей из базы данных
    users_telegram_ids = database.get_telegram_id_all_users()

    if not users_telegram_ids:
        bot.reply_to(message, "⚠️ Не удалось получить список пользователей.")
        return

    # Извлекаем ID пользователей из списка кортежей
    users_telegram_ids = [user_id[0] for user_id in users_telegram_ids]
    total_users = len(users_telegram_ids)
    delay = 1  # Задержка в секундах между отправками

    # Расчет примерного времени рассылки
    estimated_time = total_users * delay  # В секундах

    # Преобразуем в минуты и секунды
    minutes = estimated_time // 60
    seconds = estimated_time % 60

    # Уведомляем администратора о начале рассылки
    admin_message = (
        f"📣 Рассылка началась!\n"
        f"Всего пользователей: {total_users}\n"
        f"Задержка между отправками: {delay} сек\n"
        f"Примерная длительность рассылки: {minutes} мин {seconds} сек"
    )
    bot.reply_to(message, admin_message)

    # Счетчики для статистики
    successful = 0
    failed = 0

    # Рассылка сообщений
    for user_id in users_telegram_ids:
        try:
            bot.send_message(user_id, message.text)
            successful += 1
            time.sleep(delay)  # Задержка между отправками
        except Exception as e:
            if "bot was blocked by the user" in str(e):
                print(f"Пользователь {user_id} заблокировал бота.")
                #database.delete_user_by_id(user_id)  # Удаляем пользователя из базы если нужно
            else:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
            failed += 1

    # Итоговая статистика
    final_message = (
        f"✅ Рассылка завершена!\n"
        f"Успешно отправлено: {successful} пользователей\n"
        f"Ошибок: {failed}\n"
    )
    bot.reply_to(message, final_message)



