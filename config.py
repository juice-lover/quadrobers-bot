# --- config.py ---
# --- импортируем зависимости ---

from dotenv import load_dotenv
import os


load_dotenv()

"""
Используйте следующую команду для быстрой генерации значения для WEBHOOK_SECRET_PATH:

import secrets; print(secrets.token_hex())
Пример -> 192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf
"""


class BotConfiguration:
    API_TOKEN_TELEGRAM = os.getenv("API_TOKEN_TELEGRAM") # telegram token
    WEBHOOK_SECRET_PATH = os.getenv("WEBHOOK_SECRET_PATH")
    WELCOME_START_STICKER = "CAACAgIAAxkBAAENGNFnL-K5oNhn-EKq91KbNppSEs-V9AAC0wADVp29CvUyj5fVEvk9NgQ"


ConfigBotClass = BotConfiguration()