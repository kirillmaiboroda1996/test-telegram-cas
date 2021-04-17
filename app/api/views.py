from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import telebot
from app.api.wrapper import CasinoSlots
from telebot import types

token = '1682503641:AAH8liLeWDge1mr9M6tae_xbHrwT6WysfJc'
bot = telebot.TeleBot(token)

merch_id = 'c554544b6e4f7029157eb597aa951c06'
key = '3bbf5767fa84682762ff772bc78c16b14d8642a7'


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_casino_webhook(request):
    print(request.data)
    return Response('accept')


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_game_list(request):
    games = CasinoSlots(merch_id, key).get_games()
    return Response(games)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_webhook(request):
    data = request.data
    print(data)
    chat_id = data['message']['chat']['id']

    name = data['message']['from']['first_name']
    text = f'Hello {name} welcome to our casino!'

    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('a')
    itembtnv = types.KeyboardButton('v')
    itembtnc = types.KeyboardButton('c')
    itembtnd = types.KeyboardButton('d')
    itembtne = types.KeyboardButton('e')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd, itembtne)
    bot.send_message(chat_id, text, reply_markup=markup)
    return Response('hello!')


def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)

# https://telegram-casino.herokuapp.com/api/v1/webhook/


# https://api.telegram.org/bot1682503641:AAH8liLeWDge1mr9M6tae_xbHrwT6WysfJc/setWebhook?url=telegram-casino.herokuapp.com/api/v1/webhook/