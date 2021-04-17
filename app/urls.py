from django.urls import path, include
from .views import index
from .api.views import get_webhook, get_casino_webhook, get_game_list


urlpatterns = [
    path('', index),
    path('webhook/', get_webhook),
    path('webhook/casino/', get_casino_webhook),
    path('casino-bot/games/', get_game_list)

]
