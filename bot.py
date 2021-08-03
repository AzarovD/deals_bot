import telebot
from bot_config import *
from keyboard import *
from database import *

bot = telebot.TeleBot(bot_token)

reply_messages = {}   # user_id : message for reply
users_answers = {}

def show_main_keyboard(user_id):
    bot.send_message(user_id, text="Выбери действие", reply_markup=main_keyboard())


@bot.message_handler(content_types=['text'])
def greetings(message):
    if message.text == "Привет" or message.text == "/start":
        bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}, здесь ты можешь создать список дел")
    elif message.text == "Что ты умеешь?":
        bot.send_message(message.from_user.id, "Я умею всё")


    if message.reply_to_message:
        if message.reply_to_message.message_id == reply_messages[message.from_user.id]['message'].message_id:
            if reply_messages[message.from_user.id]['theme'] == 'title':
                users_answers[message.from_user.id]['title'] = message.text
                ask_deal_description(message)
            
            elif reply_messages[message.from_user.id]['theme'] == 'description':
                users_answers[message.from_user.id]['description'] = message.text
                send_ok = send_deal(message.from_user.id, users_answers[message.from_user.id]['title'], users_answers[message.from_user.id]['description'])
                if send_ok:
                    bot.send_message(message.from_user.id, "Дело успешно добавлено")
                else:
                    bot.send_message(message.from_user.id, "Произошлая ошибка. Попробуйте позже")
            
            elif reply_messages[message.from_user.id]['theme'] == 'delete':
                if message.text.isdigit:
                    deal_number = int(message.text)
                    delete_ok = delete_deal(deal_number, message.from_user.id)
                    if delete_ok:
                        bot.send_message(message.from_user.id, "Дело успешно удалено")
                    else:
                        bot.send_message(message.from_user.id, "Произошла ошибка. Верно ли указан номер?")

                else:
                    bot.send_message(message.from_user.id, "Необходимо указать только номер")


    show_main_keyboard(message.from_user.id)
 
    
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "show_deals":
        bot.send_message(call.from_user.id, get_deals(call.from_user.id)[0])
        show_main_keyboard(call.from_user.id)
        
    elif call.data == "create_deal":
        users_answers.update({call.from_user.id:{'title':None, 'description':None}})
        print(users_answers)
        ask_deal_title(call)
    
    elif call.data == "delete_deal":
        bot_message = get_deals(call.from_user.id)[0]
        bot.send_message(call.from_user.id, bot_message)
        if bot_message == "У вас пока нет дел":    
            show_main_keyboard(call.from_user.id)
            return
        else:
            msg = bot.send_message(call.from_user.id, "Выберите номер удаляемого дела")
            reply_messages.update({call.from_user.id:{'message':msg, 'theme':'delete'}})
    
    elif call.data == "edit_deal":
        bot.send_message(call.from_user.id, text="Выберите дело для редактирования", reply_markup=deals_for_edit_keyboard(call.from_user.id))
            


def ask_deal_title(call):
    msg = bot.send_message(call.from_user.id, "Введите название дела. \nНеобходимо ответить на данное сообщение")
    reply_messages.update({call.from_user.id:{'message': msg, 'theme': 'title'}})

def ask_deal_description(call):
    msg = bot.send_message(call.from_user.id, "Введите описание дела. \nНеобходимо ответить на данное сообщение")
    reply_messages.update({call.from_user.id:{'message': msg, 'theme': 'description'}})

bot.polling(none_stop=True, interval=0)




