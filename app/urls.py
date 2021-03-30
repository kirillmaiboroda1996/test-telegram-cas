from django.urls import path, include
from .views import index
from .api.views import get_webhook, get_casino_webhook
urlpatterns = [
    path('', index),
    path('webhook/', get_webhook),
    path('webhook/casino/', get_casino_webhook)

]
