from django.urls import path, include
from .api.views import get_games
urlpatterns = [
    path('games', get_games)
]
