from helpers import jsonHelper
import telebot

#Получаем данные авторизации
JIRA_URL = jsonHelper.credentials.get('JIRA_URL')
JIRA_USERNAME = jsonHelper.credentials.get('JIRA_USERNAME')
JIRA_PASSWORD = jsonHelper.credentials.get('JIRA_PASSWORD')
TELEGRAM_BOT_TOKEN = jsonHelper.credentials.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = jsonHelper.credentials.get('TELEGRAM_CHAT_ID')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)