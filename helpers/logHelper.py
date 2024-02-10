import logging

# Настройка логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Обработчик для отправки логов в Telegram
#telegram_logging_handler = TelegramLoggingHandler()
#telegram_logging_handler.setFormatter(formatter)
#logger.addHandler(telegram_logging_handler)