from django.urls import path
from .views import index, bot_messages, positions, add_user, get_user, get_admins

# admin_bot

urlpatterns = [
    path('', index, name='index'),
    path('bot_messages', bot_messages, name='bot_messages'),
    path('positions', positions, name='positions'),
    path('add_user', add_user, name='add_user'),
    path('get_user/<int:user_id>', get_user, name='get_user'),
    path('get_admins', get_admins, name='get_admins')
]
