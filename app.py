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

    user_already_exists = not database.add_user_to_db(telegram_id)
    bot.send_sticker(telegram_id, ConfigBotClass.WELCOME_START_STICKER)

    if user_already_exists:
        message_text = "Вы уже зарегистрированы.\nГлавное меню."

    else:

        text_message = ("Привет, квадробер! 🐾\n\n"
                        "Ты нашёл уникального бота, созданного специально для тех, кто живёт на четвереньках и любит имитировать повадки животных! 🚀\n\n"
                        "Мы готовим для тебя целый набор удивительных функций, которые помогут улучшить твои навыки, найти новых друзей и сделать тренировки ещё интереснее. Но пока это небольшой секрет... 😉\n\n"
                        "Совсем скоро ты сможешь испытать на себе все возможности бота! Подписывайся, оставайся с нами и будь готов к первым обновлениям. Это будет круто! 🐺✨")

        bot.reply_to(message, text_message)


# Обработка вебхука от Telegram
@app.route(f'/webhook/{ConfigBotClass.WEBHOOK_SECRET_PATH}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    print("WebHook получен")  # Проверка на получение запроса
    return 'ok', 200