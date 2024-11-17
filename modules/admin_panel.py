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
    """Функция для рассылки сообщений всем пользователям."""

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

    # Рассылаем сообщение всем пользователям
    for user_id in users_telegram_ids:
        try:
            bot.send_message(user_id, message.text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    bot.reply_to(message, "✅ Сообщение отправлено всем пользователям!")

