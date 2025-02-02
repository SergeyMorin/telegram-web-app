from flask import Flask, request
import os
from dotenv import load_dotenv
import telebot

load_dotenv()
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TELEGRAM_API_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN set for the application")
if not TELEGRAM_CHAT_ID:
    raise ValueError("No TELEGRAM_CHAT_ID set for the application")

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
app = Flask(__name__)

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not name or not phone:
        return "Ошибка: Пожалуйста, заполните все поля.", 400

    message = f"Новая заявка на консультацию:\n\nИмя: {name}\nТелефон: {phone}"

    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        return "Заявка успешно отправлена!", 200
    except Exception as e:
        return f"Ошибка при отправке сообщения: {str(e)}", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

