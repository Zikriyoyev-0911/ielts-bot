import os
from threading import Thread
from flask import Flask
import telebot
from telebot import types

# 1. Telegram Bot Tokeningiz
TOKEN = "8868930479:AAELllmp_aGLgzBMcRtsCMTTjjYzqcGUjlI"
bot = telebot.TeleBot(TOKEN)

# 2. Flask web-serveri (Render uzluksiz ishlashi va sleep mode'ga o'tib qolmasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "IELTS Bot 24/7 ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 3. /start buyrug'i - Tugmalarni chiqarish
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_listening = types.KeyboardButton("🎧 Listening")
    btn_reading = types.KeyboardButton("📖 Reading")
    btn_writing = types.KeyboardButton("✍️ Writing")
    btn_speaking = types.KeyboardButton("🗣 Speaking")
    
    markup.add(btn_listening, btn_reading, btn_writing, btn_speaking)
    
    bot.send_message(
        message.chat.id, 
        "Assalomu alaykum! Cambridge IELTS 9 tayyorgarlik botiga xush kelibsiz.\n\nKerakli bo'limni tanlang:", 
        reply_markup=markup
    )

# 4. Tugmalar bosilganda fayllarni yuborish
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id
    text = message.text

    # 🎧 LISTENING (Audio fayl yuborish)
    if text == "🎧 Listening":
        try:
            with open("audio.mp3", "rb") as audio:
                bot.send_audio(chat_id, audio, caption="🎧 Cambridge IELTS 9 - Listening Audio")
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ 'audio.mp3' fayli GitHub repositoriyasida topilmadi.")

    # 📖 READING (HTML fayl yuborish)
    elif text == "📖 Reading":
        try:
            with open("reading.html", "rb") as html_file:
                bot.send_document(chat_id, html_file, caption="📖 Cambridge IELTS 9 - Reading Material")
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ 'reading.html' fayli GitHub repositoriyasida topilmadi.")

    # ✍️ WRITING (HTML fayl yuborish)
    elif text == "✍️ Writing":
        try:
            with open("writing.html", "rb") as html_file:
                bot.send_document(chat_id, html_file, caption="✍️ Cambridge IELTS 9 - Writing Material")
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ 'writing.html' fayli GitHub repositoriyasida topilmadi.")

    # 🗣 SPEAKING (3 ta rasmni bitta albom/media-group qilib yuborish)
    elif text == "🗣 Speaking":
        try:
            img1 = open("speaking1.jpg", "rb")
            img2 = open("speaking2.jpg", "rb")
            img3 = open("speaking3.jpg", "rb")
            
            media_group = [
                types.InputMediaPhoto(img1, caption="🗣 Cambridge IELTS 9 - Speaking Practice Materials"),
                types.InputMediaPhoto(img2),
                types.InputMediaPhoto(img3)
            ]
            
            bot.send_media_group(chat_id, media_group)
            
            # Fayllarni yopish
            img1.close()
            img2.close()
            img3.close()
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ Speaking rasmlari ('speaking1.jpg', 'speaking2.jpg', 'speaking3.jpg') topilmadi.")

# 5. Bot va Flask serverini ishga tushirish
if __name__ == '__main__':
    # Flask serverni fon rejimida (Thread) ishga tushiramiz
    t = Thread(target=run_flask)
    t.start()
    
    print("Bot muvaffaqiyatli ishga tushdi!")
    bot.infinity_polling()
