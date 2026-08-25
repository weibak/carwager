from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError

from showbill.models import Advert
from .models import ChatRoom, Message


@login_required
def test_chat_auth(request):
    """Тестовая страница для проверки чата с аутентификацией"""
    return render(request, 'chat/test_auth.html')


@login_required
def open_chat(request, advert_id):
    """Открыть или создать чат с объявления"""
    try:
        advert = Advert.objects.get(id=advert_id)
    except Advert.DoesNotExist:
        return JsonResponse({'error': 'Advert not found'}, status=404)
    
    # Проверяем, что пользователь не пытается писать сам себе
    if request.user == advert.owner:
        return JsonResponse({'error': 'Вы не можете писать сами себе'}, status=400)
    
    # Создаем или получаем чат-комнату
    try:
        chat_room, created = ChatRoom.objects.get_or_create(
            advert=advert,
            user=request.user,
            defaults={'owner': advert.owner}
        )
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    # Перенаправляем на страницу чата
    from django.shortcuts import redirect
    return redirect('view_chat', chat_room_id=chat_room.id)


@login_required
def view_chat(request, chat_room_id):
    """Страница конкретного чата"""
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room not found'}, status=404)
    
    # Проверяем, что пользователь участник этого чата
    if request.user.id not in [chat_room.user_id, chat_room.owner_id]:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Помечаем сообщения как прочитанные
    chat_room.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(is_read=True)
    
    # Определяем второго участника
    other_user = chat_room.owner if chat_room.user == request.user else chat_room.user
    
    return render(request, 'chat/chat_detail.html', {
        'chat_room': chat_room,
        'other_user': other_user,
        'advert': chat_room.advert,
    })


def simple_chat(request, advert_id):
    """Простая страница чата для конкретного объявления"""
    return render(request, 'chat/simple_chat.html', {'advert_id': advert_id})


@login_required
def get_chat_room_messages(request, chat_room_id):
    """Получить все сообщения конкретного чата-комнаты"""
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    
    # Проверяем, что пользователь участник этого чата
    if request.user.id not in [chat_room.user_id, chat_room.owner_id]:
        return JsonResponse({'error': 'Access denied'}, status=403)

    # Получаем сообщения
    messages = Message.objects.filter(
        chat_room=chat_room
    ).select_related('sender').order_by('timestamp')

    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'sender_id': message.sender.id,
            'sender_username': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read,
        })

    return JsonResponse({
        'chat_room_id': chat_room.id,
        'advert_id': chat_room.advert.id,
        'advert_title': str(chat_room.advert),
        'other_user_id': chat_room.owner.id if chat_room.user == request.user else chat_room.user.id,
        'other_user_username': (chat_room.owner.username if chat_room.user == request.user else chat_room.user.username),
        'messages': messages_data,
    })


@login_required
def get_chat_messages(request):
    """Получить сообщения чата для конкретного объявления"""
    advert_id = request.GET.get('advert_id')

    if not advert_id:
        return JsonResponse({'error': 'advert_id is required'}, status=400)

    try:
        advert = Advert.objects.get(id=advert_id)
    except Advert.DoesNotExist:
        return JsonResponse({'error': 'Advert not found'}, status=404)

    # Проверяем, что пользователь не пытается писать сам себе
    if request.user == advert.owner:
        return JsonResponse({'error': 'Вы не можете писать сами себе'}, status=400)

    # Находим или создаем чат-комнату
    try:
        chat_room, created = ChatRoom.objects.get_or_create(
            advert=advert,
            user=request.user,
            defaults={'owner': advert.owner}
        )
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Получаем сообщения
    messages = Message.objects.filter(
        chat_room=chat_room
    ).select_related('sender').order_by('timestamp')

    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'sender_id': message.sender.id,
            'sender_username': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read,
        })

    return JsonResponse({
        'chat_room_id': chat_room.id,
        'advert_id': advert.id,
        'advert_title': str(advert),
        'owner_username': advert.owner.username,
        'messages': messages_data,
    })


@login_required
def get_user_chat_rooms(request):
    """Получить все чат-комнаты пользователя (как user или как owner)"""
    # Чаты, где пользователь - это user (инициатор)
    chat_rooms_as_user = ChatRoom.objects.filter(
        user=request.user
    ).select_related('advert', 'owner', 'user').order_by('-updated_at')

    # Чаты, где пользователь - это owner (продавец)
    chat_rooms_as_owner = ChatRoom.objects.filter(
        owner=request.user
    ).select_related('advert', 'owner', 'user').order_by('-updated_at')

    # Объединяем и сортируем по времени обновления
    all_chat_rooms = list(chat_rooms_as_user) + list(chat_rooms_as_owner)
    all_chat_rooms.sort(key=lambda x: x.updated_at, reverse=True)

    rooms_data = []
    for room in all_chat_rooms:
        # Определяем второго участника
        other_user = room.owner if room.user == request.user else room.user
        
        last_message = room.messages.last()
        unread_count = room.messages.filter(is_read=False).exclude(sender=request.user).count()

        rooms_data.append({
            'id': room.id,
            'advert_id': room.advert.id,
            'advert_title': str(room.advert),
            'other_user_username': other_user.username,
            'last_message': last_message.content if last_message else '',
            'last_message_time': last_message.timestamp.isoformat() if last_message else None,
            'unread_count': unread_count,
            'updated_at': room.updated_at.isoformat(),
        })

    return JsonResponse({'chat_rooms': rooms_data})


@login_required
def mark_messages_as_read(request, chat_room_id):
    """Пометить сообщения как прочитанные"""
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    
    # Проверяем, что пользователь участник этого чата
    if request.user.id not in [chat_room.user_id, chat_room.owner_id]:
        return JsonResponse({'error': 'Access denied'}, status=403)

    # Помечаем все непрочитанные сообщения (кроме своих) как прочитанные
    updated = chat_room.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(is_read=True)

    return JsonResponse({'updated_count': updated})


@login_required
def my_chats(request):
    """Страница со списком всех чатов пользователя"""
    # Чаты, где пользователь - это user (инициатор)
    chat_rooms_as_user = ChatRoom.objects.filter(
        user=request.user
    ).select_related('advert', 'owner', 'user').prefetch_related('messages').order_by('-updated_at')

    # Чаты, где пользователь - это owner (продавец)
    chat_rooms_as_owner = ChatRoom.objects.filter(
        owner=request.user
    ).select_related('advert', 'owner', 'user').prefetch_related('messages').order_by('-updated_at')

    # Объединяем чаты
    all_chat_rooms = []
    
    for room in chat_rooms_as_user:
        room.other_user = room.owner
        room.unread_count = room.messages.filter(
            is_read=False
        ).exclude(
            sender=request.user
        ).count()
        room.last_message = room.messages.last()
        all_chat_rooms.append(room)

    for room in chat_rooms_as_owner:
        room.other_user = room.user
        room.unread_count = room.messages.filter(
            is_read=False
        ).exclude(
            sender=request.user
        ).count()
        room.last_message = room.messages.last()
        all_chat_rooms.append(room)
    
    # Сортируем по времени обновления
    all_chat_rooms.sort(key=lambda x: x.updated_at, reverse=True)

    return render(request, 'chat/my_chats.html', {
        'chat_rooms': all_chat_rooms
    })
