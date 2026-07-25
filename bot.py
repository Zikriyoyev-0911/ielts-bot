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

# ⚠️ Shu yerga BotFather'dan olgan tokeningizni qo'ying:
TOKEN = '8868930479:AAELllmp_aGLgzBMcRtsCMTTjjYzqcGUjlI'
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
        "Xush kelibsiz! **Cambridge IELTS 9 - Test 1** materiallarini ko'rish uchun kerakli bo'lim tugmasini bosing:", 
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == '🎧 Listening')
def send_listening(message):
    text = """🎧 **Cambridge IELTS 9 - Test 1: Listening**

📌 **Section 1: Job Enquiry**
1. answer(ing) (the) phone | 2. Hillsdunne Road | 3. library
4. 4.45 | 5. national holidays | 6. after 11 (o'clock)
7. clear voice | 8. think quickly | 9. 22 October | 10. Manuja

📌 **Section 2: Sports World**
11. branch | 12. west | 13. clothing | 14. 10 | 15. running
16. bags | 17. A | 18. A | 19-20. A, E

📌 **Section 3: Course Feedback**
21. B | 22. C | 23. B | 24. A | 25. C
26. B | 27. A | 28. B | 29. C | 30. B

📌 **Section 4: Whales & Dolphins**
31. tide/tides | 32. hearing/ear/ears | 33. plants / animals/fish/fishes
34. feeding | 35. noise/noises | 36. healthy | 37. group
38. social | 39. leader | 40. network/networks"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '📖 Reading')
def send_reading(message):
    text = """📖 **Cambridge IELTS 9 - Test 1: Reading**

📌 **Passage 1: William Henry Perkin**
• **Mavzu:** Ilk sintetik bo'yoq kashfiyoti va Perkin hayoti.
• **Savol turlari:** True/False/Not Given, Diagram, Short Answer.

📌 **Passage 2: Is Everybody Having Fun?**
• **Mavzu:** Ish joyidagi psixologiya va ruhiy holat.
• **Savol turlari:** Matching Headings, Summary, Multiple Choice.

📌 **Passage 3: The Concept of Intelligence**
• **Mavzu:** Inson intellekti va psixometriya.
• **Savol turlari:** Matching Information, True/False/Not Given, Multiple Choice."""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '✍️ Writing')
def send_writing(message):
    text = """✍️ **Cambridge IELTS 9 - Test 1: Writing**

📊 **Task 1 (Line Graph):**
Yillar davomida ma'lum bir hududdagi aholining yosh guruhlari bo'yicha foiz ko'rsatkichlari o'zgarishini tasvirlash.

📝 **Task 2 (Discussion Essay):**
*"Some people think that universities should provide graduates with the knowledge and skills needed in the workplace. Others think that the true function of a university should be to give access to knowledge for its own sake, regardless of whether the course is useful to an employer. Discuss both views and give your opinion."*"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🗣️ Speaking')
def send_speaking(message):
    text = """🗣️ **Cambridge IELTS 9 - Test 1: Speaking**

🔹 **Part 1:**
• Telephoning | Games | Daily Routine

🔹 **Part 2 (Cue Card):**
> *"Describe a person who has done a lot of work to help people."*

🔹 **Part 3 (Discussion):**
• Jamiyatda xayriya va o'zaro yordam.
• Ko'ngillilik (volunteering) harakatining ahamiyati."""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.polling(none_stop=True)
