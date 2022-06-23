from django.urls import path
# from django.conf import settings


from webbot import views

urlpatterns = [
    path('', views.main, name='bothome'),
    
]
