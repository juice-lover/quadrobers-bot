# --- app.py ---
# --- импортируем зависимости ---

from config import ConfigBotClass
import telebot

from flask import Flask, request
from modules import database, keyboard, admin_panel
from telebot import types


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
def admin_panel_func(message):
    telegram_id = message.from_user.id  # Получаем ID пользователя Telegram
    is_admin = telegram_id == ConfigBotClass.TELEGRAM_ID_ADMIN # Проверяем, является ли пользователь администратором

    if is_admin:
        # Отправляем админ-панель
        admin_panel.send_admin_panel_to_admin(bot, message)
    else:
        # Сообщаем пользователю об отказе в доступе
        bot.reply_to(message, "🚫 В доступе отказано!")


# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: call.data == "send_msg_all_users_button")
def send_msg_all_users(call):
    # Удаляем предыдущее сообщение
    bot.delete_message(call.message.chat.id, call.message.message_id)
    telegram_id = call.from_user.id
    is_admin = telegram_id == ConfigBotClass.TELEGRAM_ID_ADMIN  # Проверяем, является ли пользователь администратором

    if is_admin:

        # генерируем кнопку
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        cancel_button = types.KeyboardButton(text="Отменить операцию")
        markup.add(cancel_button)

        bot.send_message(telegram_id, "Отправьте ваше сообщение, чтобы начать рассылку:")
        # Ожидаем сообщение от админа и передаем аргументы в функцию
        bot.register_next_step_handler(call.message, lambda message: admin_panel.send_msg_all_users_function(bot, message))
    else:
        # Сообщаем пользователю об отказе в доступе
        bot.send_message(telegram_id, "🚫 В доступе отказано!")