from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from telebot.apihelper import send_message


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_casino_webhook(request):
    print(request.data)
    return Response('accept')


@api_view(['POST'])
def get_webhook(request):
    data = request.data
    print(data)
    chat_id = data['message']['chat']['id']
    message = data['message']['text']
    name = data['message']['from']['first_name']

    text = f'Hello {name} welcome to our casino!'
    token = 'bot1682503641:AAEXVqQYzuox0rlOSkENYw_4n91BgZnPYfE'
    if 'casino' in message:
        send_message(token, chat_id, text)
    return Response('hello!')


# https://telegram-casino.herokuapp.com/api/v1/webhook/


# https://api.telegram.org/bot1682503641:AAEXVqQYzuox0rlOSkENYw_4n91BgZnPYfE/setWebhook?url=telegram-casino.herokuapp.com/api/v1/webhook/