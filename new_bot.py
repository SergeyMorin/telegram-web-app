import os
from dotenv import load_dotenv
import telebot

load_dotenv()

api_token = os.getenv('TELEGRAM_BOT_TOKEN')

print(f"API Token from environment: {api_token}")

if not api_token:
    raise ValueError("No TELEGRAM_BOT_TOKEN set for the application")

bot = telebot.TeleBot(api_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Welcome to the new project.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
