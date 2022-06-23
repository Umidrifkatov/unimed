
from django.contrib import admin
from django.urls import path, include
from telegram_bot.views import worker
from django.conf import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('webbot/', include('webbot.urls')),
    path('admin/', admin.site.urls),
    path(f'telegram/{settings.TOKEN}/', worker, name="bot"),
    path('', include('website.urls')),
    
]







