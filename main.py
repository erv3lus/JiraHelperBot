import handlers
from helpers import authHelper, dbHelper, logHelper

import sys
import threading
class TelegramLoggingHandler(logHelper.logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        authHelper.bot.send_message(authHelper.TELEGRAM_CHAT_ID, log_entry)

# Обработчики команд
@authHelper.bot.message_handler(commands=['start'])
def send_welcome(message):
    handlers.send_welcome(message)

@authHelper.bot.message_handler(commands=['tasks'])
def get_my_tasks(message):
    handlers.get_tasks(message)

@authHelper.bot.message_handler(commands=['update_comments'])
def update_comments(message):
    logHelper.logger.info(f'Получена команда /update_comments от пользователя {message.from_user.username}')
    # Вызов функции check_for_new_comments для запроса обновлений комментариев
    handlers.update_comments()

@authHelper.bot.message_handler(commands=['update_status'])
def update_comments(message):
    logHelper.logger.info(f'Получена команда /update_status от пользователя {message.from_user.username}')
    # Вызов функции check_for_new_comments для запроса обновлений комментариев
    handlers.update_status()

@authHelper.bot.message_handler(commands=['update_tasks'])
def update_tasks(message):
    logHelper.logger.info(f'Получена команда /update_tasks от пользователя {message.from_user.username}')
    # Вызов функции check_for_new_comments для запроса обновлений комментариев
    handlers.update_tasks()


def sсhedule_tasks():
    try:
        handlers.update_comments()
        handlers.update_tasks()
        handlers.update_status()

    finally:
        threading.Timer(60, sсhedule_tasks).start()


def main():
    dbHelper.create_table()
    sсhedule_tasks()
    authHelper.bot.polling()  # Запуск бота


if __name__ == "__main__":
    main()
