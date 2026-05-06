from django.urls import path
from .views import create_event, user_login

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('user/', user_login, name='login')
]
