# --- app.py ---
# --- импортируем зависимости ---

from config import ConfigBotClass
import telebot

from flask import Flask, request
from modules import database


# Инициализация бота
bot = telebot.TeleBot(ConfigBotClass.API_TOKEN_TELEGRAM, threaded=False)
app = Flask(__name__)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id  # Получаем ID пользователя Telegram

    # Попытка добавить пользователя в базу данных если его еще нет
    user_already_exists = database.add_user_to_db(telegram_id)

    # Отправка стикера приветствия
    bot.send_sticker(message.chat.id, ConfigBotClass.WELCOME_START_STICKER)

    # Приветственное сообщение для новых пользователей
    message_text = (
        "Привет, квадробер! 🐾\n\n"
        "Ты нашёл уникального бота, созданного специально для тех, кто живёт на четвереньках и любит имитировать повадки животных! 🚀\n\n"
        "Мы готовим для тебя целый набор удивительных функций, которые помогут улучшить твои навыки, найти новых друзей и сделать тренировки ещё интереснее. Но пока это небольшой секрет... 😉\n\n"
        "Совсем скоро ты сможешь испытать на себе все возможности бота! Подписывайся, оставайся с нами и будь готов к первым обновлениям. Это будет круто! 🐺✨"
    )

    # Отправка текстового сообщения пользователю
    bot.reply_to(message, message_text)


# Обработка вебхука от Telegram
@app.route(f'/webhook/{ConfigBotClass.WEBHOOK_SECRET_PATH}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    print("WebHook получен")  # Проверка на получение запроса
    return 'ok', 200


@bot.message_handler(commands=['a'])
def admin_panel(message):
    telegram_id = message.from_user.id  # Получаем ID пользователя Telegram

    # Проверка, является ли пользователь администратором
    if telegram_id == ConfigBotClass.TELEGRAM_ID_ADMIN:
        try:
            # Получаем количество пользователей из базы данных
            number_of_users = database.get_number_of_users()

            # Формируем сообщение для админа
            text_message = (f"Админ панель\n\n"
                            f"Количество пользователей: {number_of_users}")

            bot.reply_to(message, text_message)

        except Exception as e:
            # Обработка возможных ошибок
            bot.reply_to(message, "Произошла ошибка при получении данных.")
            print(f"Ошибка в админ панели: {e}")
