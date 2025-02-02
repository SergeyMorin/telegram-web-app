import os
from dotenv import load_dotenv
import telebot
from telebot import types
from flask import Flask, request, jsonify
import threading


load_dotenv()
api_token = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not api_token:
    raise ValueError("No TELEGRAM_BOT_TOKEN set for the application")
if not TELEGRAM_CHAT_ID:
    raise ValueError("No TELEGRAM_CHAT_ID set for the application")

bot = telebot.TeleBot(api_token)
app = Flask(__name__)

# WEBHOOK_URL = "https://66.151.40.169/webhook" # server https://66.151.40.169 # lan https://127.0.0.1:5000/webhoo
# bot.remove_webhook()
# bot.set_webhook(url=WEBHOOK_URL)

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     json_str = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_str)
#     bot.process_new_updates([update])
#     return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    web_app_button = types.InlineKeyboardButton("Открыть Web App",
                                                url="https://sergeymorin.github.io/telegram-web-app/")
    markup.add(web_app_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы открыть Web App.", reply_markup=markup)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not name or not phone:
        return jsonify({"success": False, "message": "Ошибка: Пожалуйста, заполните все поля."}), 400

    message = f"Новая заявка на консультацию:\n\nИмя: {name}\nТелефон: {phone}"

    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        return jsonify({"success": True, "message": "Заявка успешно отправлена!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка при отправке сообщения: {str(e)}"}), 500


def run_bot():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    # bot.remove_webhook()
    # bot.set_webhook(url=WEBHOOK_URL)

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
