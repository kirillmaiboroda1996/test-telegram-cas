from datetime import datetime
from django.conf import settings
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import CasinoService

CASINO_MERCH_ID = 'kirill.io'
CASINO_URL = 'qweqweqweq123123'


@api_view(['GET'])
def get_games(request):
    casino = CasinoService().get_casino(CASINO_MERCH_ID, CASINO_URL)
    games = casino.get_games()
    return Response(games)
