from django.urls import path
from . import views

urlpatterns = [
    path('api/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('api/rooms/', views.get_user_chat_rooms, name='get_user_chat_rooms'),
    path('api/rooms/<int:chat_room_id>/read/', views.mark_messages_as_read, name='mark_messages_read'),
    path('api/rooms/<int:chat_room_id>/messages/', views.get_chat_room_messages, name='get_chat_room_messages'),
    path('my/', views.my_chats, name='my_chats'),
    path('open/<int:advert_id>/', views.open_chat, name='open_chat'),
    path('<int:chat_room_id>/', views.view_chat, name='view_chat'),
]
