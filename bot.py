import telebot
from bot_config import *
from keyboard import *
from database import *

bot = telebot.TeleBot(bot_token)

reply_messages = {}

def show_main_keyboard(user_id):
    bot.send_message(user_id, text="Выбери действие", reply_markup=main_keyboard())





@bot.message_handler(content_types=['text'])
def greetings(message):
    if message.text == "Привет" or message.text == "/start":
        bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}, здесь ты можешь создать список дел")
    elif message.text == "Что ты умеешь?":
        bot.send_message(message.from_user.id, "Я умею всё")
    else:
        bot.send_message(message.from_user.id, "Я не знаю такой команды")
	

    if message.reply_to_message:
        if message.reply_to_message.message_id == reply_messages[message.from_user.id]:
            create_deal(message)


    show_main_keyboard(message.from_user.id)
    





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "show_deals":
        bot.send_message(call.from_user.id, get_deals(call.from_user.id))
        show_main_keyboard(call.from_user.id)

    if call.data == "create_deal":
        msg = bot.send_message(call.from_user.id, "Введите название дела. Необходимо разделить название и описание символом \\")
        reply_messages.update({call.from_user.id:msg.message_id})



def create_deal(message):
    deal_title = message.text.split('\\')[0]
    if '\\' in message.text:
        deal_descr = message.text.split('\\')[1] 
    reply_msg = send_deal(message.from_user.id, deal_title, deal_descr)
    bot.send_message(message.from_user.id, reply_msg)
    show_main_keyboard(message.from_user.id)


bot.polling(none_stop=True, interval=0)




