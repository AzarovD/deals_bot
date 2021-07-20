import telebot
from telebot import types

def main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    show_deals_btn = types.InlineKeyboardButton("Показать дела", callback_data="show_deals")
    create_deal_btn = types.InlineKeyboardButton("Добавить дело", callback_data="create_deal")
    edit_deals_btn = types.InlineKeyboardButton("Изменить дела", callback_data="edit_deals")
    delte_deal_btn = types.InlineKeyboardButton("Удалить дело", callback_data="delete_deal")
    buttons = [show_deals_btn, create_deal_btn, edit_deals_btn, delte_deal_btn]
    for button in buttons:
        keyboard.add(button)
    return keyboard