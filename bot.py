import telebot
import os
from pydub import AudioSegment
import re

bot = telebot.TeleBot("ТОКЕН")

flag_voice=False
flag_photo=False
flag_urls=False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "привет")
    bot.send_message(message.chat.id, "пришли мне сначала аудио")

@bot.message_handler(content_types=['voice', 'photo', 'text'])
def voice(message):
    global flag_voice
    global flag_photo
    global flag_urls
    if str (message.content_type)=='voice':
        if flag_voice==False:
           bot.forward_message(chat_id=АЙДИ, from_chat_id=message.chat.id, message_id=message.message_id)
           flag_voice=True
           bot.reply_to(message, "ок, пришли фото")
        elif flag_voice==True and flag_photo==False:
           bot.reply_to(message, "ты уже прислал аудио, пришли фото")
        elif flag_voice==True and flag_photo==True:
           bot.reply_to(message, "пришли ссылку")
    if str (message.content_type)=='photo':
        if flag_voice and flag_photo==False:
            bot.forward_message(chat_id=АЙДИ, from_chat_id=message.chat.id, message_id=message.message_id)
            bot.reply_to(message, "ок, пришли ссылку") 
            flag_photo=True
        elif flag_voice==False and flag_photo==False:
            bot.reply_to(message, "неправильно, пришли аудио")
        elif flag_voice==True and flag_photo==True:
           bot.reply_to(message, "пришли ссылку")
    if str (message.content_type)=='text':
        if flag_photo:
             url_pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
             urls = re.findall(url_pattern, message.text)
             flag_url=False
             for url in urls:
                 if 'yandex' in url.lower() and 'maps' in url.lower():
                     flag_url=True
                     bot.forward_message(chat_id=АЙДИ, from_chat_id=message.chat.id, message_id=message.message_id)
             if flag_url==False:
                 bot.reply_to(message, "пришли ссылку") 
             else: 
                 bot.reply_to(message, "Спасибо за ссылку!")
                 bot.send_message(message.chat.id, "теперь ты можешь начать заново")
                 flag_voice=False
                 flag_photo=False
                 flag_urls=False
                 bot.send_message(message.chat.id, "пришли мне сначала аудио")
        else:
             bot.reply_to(message, "неправильно")

@bot.message_handler(content_types=['document', 'video', 'animation', 'sticker', 'video_note', 'contact', 'location'])
def handle_files(message):
    bot.reply_to(message, "неправильно")

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    global flag_voice
    global flag_photo
    if flag_voice==False:
        file_info = bot.get_file(message.audio.file_id)
        file_path = file_info.file_path
    
        downloaded_file = bot.download_file(file_path)
    
        with open('input.mp3', 'wb') as audio_file:
            audio_file.write(downloaded_file)
    
        audio = AudioSegment.from_file('input.mp3', format='mp3')
        audio.export('output.ogg', format='ogg')

        target_user_id = АЙДИ  
        with open('output.ogg', 'rb') as audio_file:
             bot.send_audio(target_user_id, audio_file, title='Audio', performer='Performer', thumb=None, parse_mode=None)
             flag_voice=True
             bot.reply_to(message, "ок, пришли фото")
    
        os.remove('input.mp3')
        os.remove('output.ogg')

    elif flag_voice==True and flag_photo==False:
        bot.reply_to(message, "ты уже прислал аудио, пришли фото")

bot.polling()
