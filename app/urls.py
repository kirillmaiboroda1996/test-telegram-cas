from django.urls import path, include
from .views import index
from .api.views import get_webhook
urlpatterns = [
    path('', index),
    path('webhook/', get_webhook)
]
