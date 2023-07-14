import telebot
import re

bot = telebot.TeleBot("ТОКЕН")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "привет, пришли мне аудио, фото и ссылку")

@bot.message_handler(content_types=['voice'])
def voice(message):
    bot.reply_to(message, "Спасибо за аудио!")

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.reply_to(message, "Спасибо за фото!")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    url_pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
    urls = re.findall(url_pattern, message.text)
    for url in urls:
        if 'yandex' in url.lower() and 'maps' in url.lower():
            bot.reply_to(message, "Спасибо за ссылку!")
    bot.reply_to(message, "Попробуй еще")

@bot.message_handler(content_types=['document', 'video', 'animation', 'sticker', 'video_note', 'contact', 'location', 'text'])
def handle_files(message):
    bot.reply_to(message, "Попробуй еще")

bot.polling()
