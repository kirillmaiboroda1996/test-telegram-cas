from datetime import datetime
from django.conf import settings
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import CasinoService



def index(request):
    return render(request, 'index.html')
