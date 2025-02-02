import os
from dotenv import load_dotenv
import telebot
from telebot import types
from flask import Flask, request

load_dotenv()
api_token = os.getenv('TELEGRAM_BOT_TOKEN')

if not api_token:
    raise ValueError("No TELEGRAM_BOT_TOKEN set for the application")

bot = telebot.TeleBot(api_token)
app = Flask(__name__)

WEBHOOK_URL = "https://66.151.40.169/webhook"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    web_app_button = types.InlineKeyboardButton("Открыть Web App",
                                                url="https://sergeymorin.github.io/telegram-web-app/")
    markup.add(web_app_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы открыть Web App.", reply_markup=markup)


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=5000, debug=True)
