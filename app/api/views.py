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
casino = CasinoSlots(merch_id, key)

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
    file_id = None
    callback_data = ''
    message_id = None
    game = None
    inline_message_id = None
    callback_query_id = None
    c_type = None
    media_type = None
    caption = ''

    if 'callback_query' in update:

        chat_id = update["callback_query"]["from"]["id"]
        message_id = update['callback_query']['message']['message_id']
        callback_query_id = update['callback_query']['id']

        if 'game_short_name' in update["callback_query"]:
            game = update['callback_query']["game_short_name"]
        else:
            callback_data = update["callback_query"]["data"]

    elif 'message' in update:

        if 'text' in update['message']:

            text = update['message']['text']
            chat_id = update["message"]["chat"]["id"]
        else:
            return Response('OK')

    else:
        return Response('OK')

    if text.startswith('/start'):
        keyboard = get_main_keyboard()
        bot.send_message(chat_id, text, reply_markup=keyboard)

    if text == '🎰 Список игр 🎰':
        games = casino.get_games()
        keyboard = get_game_keyboards(games)
        bot.send_message(chat_id, 'Доступные игры', reply_markup=keyboard)

    if callback_data.startswith('game_'):
        game = callback_data[5:]
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text='бесплатно', callback_data=f'demo_{game}'))
        bot.send_game(chat_id, game_short_name=game, reply_markup=keyboard)
        return Response('OK')

    if callback_data.startswith('demo_'):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text='Играть бесплатно', callback_game=game))
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        return Response('OK')
    if game:
        games = casino.get_games()
        game_uuid = get_game_uid(game, games)
        game_url = casino.create_demo_game(game_uuid=game_uuid)['url']
        bot.answer_callback_query(callback_query_id=callback_query_id, url=game_url)
        return Response('OK')


def get_main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('🎰 Список игр 🎰')
    return keyboard


def get_game_keyboards(games):
    game_list = [game['name'] for game in games['items']][:5]

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = list()
    print(buttons)
    for game in game_list:
        buttons.append(telebot.types.InlineKeyboardButton(text=game, callback_data=f'game_{game}'))

    keyboard.add(*buttons)
    return keyboard

# https://telegram-casino.herokuapp.com/api/v1/webhook/


# https://api.telegram.org/bot1682503641:AAH8liLeWDge1mr9M6tae_xbHrwT6WysfJc/setWebhook?url=telegram-casino.herokuapp.com/api/v1/webhook/

def get_game_uid(game_name, games):
    game_list = [game['uuid'] for game in games['items'] if game['name'] == game_name]
    return game_list[0]