import requests 
import json

from requests.api import delete
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

    return (message_text, deals)


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


def delete_deal(deal_number, user_id):
    get_url = "https://dealsbot-0be1.restdb.io/rest/deals?q={}&filter=" + str(user_id)
    response = requests.request("GET", get_url, headers=headers)
    deals = json.loads(response.text)
    if deal_number in range(0, len(deals)+1):
        delete_id = deals[deal_number-1]['_id']
        delete_url = f"https://dealsbot-0be1.restdb.io/rest/deals/{delete_id}"
        response = requests.request("DELETE", delete_url, headers=headers)
        if response.ok:
            return True
        else:
            return False
    else:
        return False

