from telebot import types


# Функция для создания кнопок в inline-режиме для админ панели
def create_inline_admin_buttons():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сделать рассылку", callback_data="send_msg_all_users_button")

    # Добавляем каждую кнопку отдельно, чтобы они шли вертикально
    markup.add(button1)

    return markup