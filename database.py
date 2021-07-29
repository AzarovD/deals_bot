import requests 
import json
from bot_config import *


def get_deals(user_id):
    url = "https://dealsbot-0be1.restdb.io/rest/deals?q={}&filter=" + str(user_id)
    response = requests.request("GET", url, headers=headers)
    deals = json.loads(response.text)
    message_text = ""
    for number, deal in enumerate(deals):
        message_text += f"{number+1}. Название: {deal['Title']}\n" \
                       f"Описание: {deal['Description']}\n {'-'*30}\n"
    if message_text == "":
        message_text = "У вас пока нет дел"

    return message_text


def send_deal(user_id, deal_title, deal_descr):
    url = "https://dealsbot-0be1.restdb.io/rest/deals"
    payload = json.dumps( {"Title": deal_title, 
                            "Description": deal_descr, 
                             "UserId":user_id} )
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.ok:
        return "Дело успешно добавлено"
    else:
        return "Произошла ошибка. Попробуйте позже."
