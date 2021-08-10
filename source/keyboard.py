import telebot
from telebot import types
from database import *

def main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    show_deals_btn = types.InlineKeyboardButton("Показать дела", callback_data="show_deals")
    create_deal_btn = types.InlineKeyboardButton("Добавить дело", callback_data="create_deal")
    edit_deals_btn = types.InlineKeyboardButton("Изменить дело", callback_data="edit_deal")
    delete_deal_btn = types.InlineKeyboardButton("Удалить дело", callback_data="delete_deal")
    buttons = [show_deals_btn, create_deal_btn, edit_deals_btn, delete_deal_btn]
    for button in buttons:
        keyboard.add(button)
    return keyboard


def deals_for_edit_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    deals = get_deals(user_id)[1]
    for deal in deals:
        btn = types.InlineKeyboardButton(deal['Title'], callback_data=deal['_id'])
        keyboard.add(btn)
    return keyboard
