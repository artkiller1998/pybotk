# -*- coding: utf-8 -*-
import telebot
import requests
import re
import os


keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('📱 (Phone / Pad)', '🖥️ (Pc / Tv)', '')

keyboard1_1 = telebot.types.ReplyKeyboardMarkup(True, True)
cat_tvpc = [ 'tv',  '1366x768',  '1920x1080',  '2048x1152',
'2560x1080',  '2560x1440',  '3440x1440', '3840x1080',
'ultrawide',  'oled',  '4k', '8k' ]
keyboard1_1.row('tv',  '1366x768',  '1920x1080',  '2048x1152')
keyboard1_1.row('2560x1080',  '2560x1440',  '3440x1440', '3840x1080')
keyboard1_1.row('ultrawide',  'oled',  '4k', '8k')

keyboard1_2 = telebot.types.ReplyKeyboardMarkup(True, True)
cat_phones = [ 'android',  'pixel',  'live',  'keyboard',
'iphone-xs-max',  'iphone-xs',  'iphone-xr', 'ipad',
'iphone-7-plus',  'phone-7',  'iphone-6s', 'iphone-6' ]
keyboard1_2.row('android',  'pixel',  'live',  'keyboard')
keyboard1_2.row('iphone-xs-max',  'iphone-xs',  'iphone-xr', 'ipad')
keyboard1_2.row('iphone-7-plus',  'phone-7',  'iphone-6s', 'iphone-6')

keyboard1_3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1_3.row('Select another device 🔄', 'Next  ▶️')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello, friend! Please select type of your device.", reply_markup=keyboard1)
    
@bot.message_handler(commands=['change'])
def change_device(message):
    bot.send_message(message.chat.id, "Please select type of your device.", reply_markup=keyboard1)
    tvpc_photos_group = set()
    phones_photos_group = set()
    page_counter = []
    

tvpc_photos_group = set()
phones_photos_group = set()
page_counter = []
    
def category_sender(message):
    global category
   # if message.text in cat_tvpc:
      #  category = message.text
        #bot.send_message(message.chat.id, 'TVPC')
        #tvpc_photos_group = requests.get('https://unsplash.com/napi/landing_pages/backgrounds/phone/'+ message.text +'?page='+str( len(page_counter) )+'&per_page=30').text['photos']
        #print(r)
    if message.text in cat_phones or message.text in cat_tvpc:   
        category = message.text        
        bot.send_message(message.chat.id, 'Please wait untill the preview and the file will be loaded ⌛️')
        if len(phones_photos_group) == 0 :
            page_counter.append('1')
            if message.text in cat_phones:
                req = requests.get('https://unsplash.com/napi/landing_pages/backgrounds/phone/'+ message.text +'?page='+str( len(page_counter) )+'&per_page=30').text
            else :
                req = requests.get('https://unsplash.com/napi/landing_pages/wallpapers/screen/'+ message.text +'?page='+str( len(page_counter) )+'&per_page=30').text
            phones_photos_group.update(phones_photos_group.union(set (re.findall(r'full":"(.+?)"', req) ) ))
        #print((phones_photos_group))
        #print(len(phones_photos_group))
        #print(phones_photos_group.pop())
        photo_url = phones_photos_group.pop()
        photo_id = re.search(r'photo-(.+)\?', photo_url).group(0)[:-1]
        
        subdir = './photos/'
        if not os.path.exists(subdir):
            os.mkdir(subdir)
            
        print(photo_id)
        print(photo_url)
        #bot.send_message(message.chat.id, photo_url)
        response = requests.get(photo_url)
        path_to_file = subdir + photo_id + '.jpeg'
        if not os.path.exists(path_to_file) :
            with open(path_to_file, 'wb') as out_file:
                out_file.write(response.content)
        
        with open(path_to_file, 'rb') as out_file:
            try:
                bot.send_photo(message.chat.id, photo_url)
            except:
                pass
            bot.send_document(message.chat.id, out_file, reply_markup=keyboard1_3)
    else :
        bot.send_message(message.chat.id, 'Sorry?')
        
        
@bot.message_handler(content_types=['text'])
def send_text(message):
    global page_counter
    if message.text == '🖥️ (Pc / Tv)':
        bot.send_message(message.chat.id, 'Choose one from menu:',  reply_markup=keyboard1_1)
    elif message.text == '📱 (Phone / Pad)':
        bot.send_message(message.chat.id, 'Choose one from menu:', reply_markup=keyboard1_2)
    elif message.text == 'Select another device 🔄':
        change_device(message)
    elif message.text == 'Next  ▶️':
        message.text = category
        category_sender(message)
    else:
        category_sender(message)
        
        
        
        
        
bot.polling(none_stop=True)
