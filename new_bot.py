import os
from dotenv import load_dotenv
import telebot
from telebot import types


load_dotenv()

api_token = os.getenv('TELEGRAM_BOT_TOKEN')

print(f"API Token from environment: {api_token}")

if not api_token:
    raise ValueError("No TELEGRAM_BOT_TOKEN set for the application")

bot = telebot.TeleBot(api_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    web_app_button = types.InlineKeyboardButton("Открыть Web App",
                                                url="https://sergeymorin.github.io/telegram-web-app/")
    markup.add(web_app_button)

    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы открыть Web App.", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
