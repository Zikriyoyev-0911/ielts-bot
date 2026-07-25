import os
import threading
from flask import Flask
import telebot
from telebot import types

# Render o'chirib qo'ymasligi uchun Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Bot Father'dan olgan tokeningiz
TOKEN = '8868930479:AAEl1mp_aGLgzBMcRtsCMTTjYzqcGUjLI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🎧 Listening')
    btn2 = types.KeyboardButton('📖 Reading')
    btn3 = types.KeyboardButton('✍️ Writing')
    btn4 = types.KeyboardButton('🗣️ Speaking')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Xush kelibsiz! **Cambridge IELTS 9** materiallarini ko'rish uchun kerakli bo'lim tugmasini bosing:",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    chat_id = message.chat.id
    text = message.text

    # 🎧 LISTENING (1 ta Audio + 1 ta Test PDF + 1 ta Javoblar PDF)
    if text == "🎧 Listening":
        try:
            # 1. Audio fayl
            with open("audio.mp3", "rb") as audio:
                bot.send_audio(chat_id, audio, caption="🎧 Cambridge IELTS 9 - Listening Audio")
            
            # 2. Test PDF
            with open("listening_test.pdf", "rb") as test_doc:
                bot.send_document(chat_id, test_doc, caption="📄 Listening Test (Savollar)")
            
            # 3. Javoblar PDF
            with open("listening_answers.pdf", "rb") as answers_doc:
                bot.send_document(chat_id, answers_doc, caption="✅ Listening Answers (Javoblar)")

        except FileNotFoundError as e:
            bot.send_message(chat_id, f"❌ Fayl topilmadi: '{e.filename}'\nIltimos, GitHub'ga faylni yuklaganingizni tekshiring.")

    # 📖 READING (HTML hujjat)
    elif text == "📖 Reading":
        try:
            with open("reading.html", "rb") as doc:
                bot.send_document(chat_id, doc, caption="📖 Cambridge IELTS 9 - Reading Material")
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ 'reading.html' fayli GitHub repositoriyasida topilmadi.")

    # ✍️ WRITING (HTML hujjat)
    elif text == "✍️ Writing":
        try:
            with open("writing.html", "rb") as doc:
                bot.send_document(chat_id, doc, caption="✍️ Cambridge IELTS 9 - Writing Material")
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ 'writing.html' fayli GitHub repositoriyasida topilmadi.")

    # 🗣️ SPEAKING (3 ta Rasm albomi)
    elif text == "🗣️ Speaking":
        try:
            img1 = open("speaking1.jpg", "rb")
            img2 = open("speaking2.jpg", "rb")
            img3 = open("speaking3.jpg", "rb")

            media = [
                types.InputMediaPhoto(img1, caption="🗣️ Cambridge IELTS 9 - Speaking Material"),
                types.InputMediaPhoto(img2),
                types.InputMediaPhoto(img3)
            ]
            bot.send_media_group(chat_id, media)

            img1.close()
            img2.close()
            img3.close()
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ Speaking rasmlari ('speaking1.jpg', 'speaking2.jpg', 'speaking3.jpg') topilmadi.")

if __name__ == "__main__":
    # Flask serverni alohida oqimda (thread) ishga tushirish
    threading.Thread(target=run_flask).start()
    # Botni ishga tushirish
    bot.polling(none_stop=True)
