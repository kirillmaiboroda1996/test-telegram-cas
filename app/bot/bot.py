import requests

BASE_URL = 'https://api.telegram.org/bot1682503641:AAEXVqQYzuox0rlOSkENYw_4n91BgZnPYfE/'

# bot = telebot.TeleBot("1602312085:AAFBIp2r5ZYSiOCK-mx0UGBYTaULfv5SzCo", parse_mode=None)


def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


