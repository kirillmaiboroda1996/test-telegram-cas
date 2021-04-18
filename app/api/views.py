import json

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
@bot.message_handler(commands=['start', 'help'])
def get_webhook(request):
    update = json.loads(request.body)
    text = ''
    chat_id = update["message"]["chat"]["id"]

    if 'callback_query' in update:
        pass

    elif 'message' in update:

        if 'text' in update['message']:
            text = update['message']['text']

            if text.startswith('/start'):
                keyboard = get_main_keyboard()
                bot.send_message(chat_id, text, reply_markup=keyboard)

    if text == '🎰 Список игр 🎰':
        games = CasinoSlots(merch_id, key).get_games()
        get_game_keyboards(games)
        bot.send_message(chat_id, 'Доступные игры')

    return Response('hello!')


def get_main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('🎰 Список игр 🎰')
    return keyboard


def get_game_keyboards(games):
    game_list = [game['name'] for game in games['items'][0]][:5]

    keyboard = telebot.types.InlineKeyboardMarkup()

    for item in game_list:
        keyboard.add(telebot.types.InlineKeyboardButton(text=item, callback_game='yes'))

# https://telegram-casino.herokuapp.com/api/v1/webhook/


# https://api.telegram.org/bot1682503641:AAH8liLeWDge1mr9M6tae_xbHrwT6WysfJc/setWebhook?url=telegram-casino.herokuapp.com/api/v1/webhook/
