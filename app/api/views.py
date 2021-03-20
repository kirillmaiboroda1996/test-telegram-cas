from datetime import datetime
from django.conf import settings
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import CasinoService
import requests


BASE_URL = 'https://api.telegram.org/bot1682503641:AAEXVqQYzuox0rlOSkENYw_4n91BgZnPYfE/'


def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


@api_view(['POST'])
def get_webhook(request):
    data = request.data
    chat_id = data['message']['chat']['id']
    message = data['message']['text']
    name = data['message']['from']['first_name']

    text = f'Hello {name} welcome to our casino!'

    if 'casino' in message:
        send_message(chat_id, text)
    return Response('hello!')


# https://telegram-casino.herokuapp.com/api/v1/webhook/


# https://api.telegram.org/bot1682503641:AAEXVqQYzuox0rlOSkENYw_4n91BgZnPYfE/setWebhook?url=telegram-casino.herokuapp.com/api/v1/webhook/