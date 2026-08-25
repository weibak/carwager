import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"🔗 WebSocket connect attempt")

        self.chat_room_id = self.scope['url_route']['kwargs'].get('chat_room_id')
        print(f"   Chat Room ID: {self.chat_room_id}")

        # Получаем пользователя
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            print("   ❌ User not authenticated, closing connection")
            await self.close(code=4001)  # Custom code for auth error
            return

        print(f"   👤 User: {self.user.username} (ID: {self.user.id})")

        try:
            # Получаем чат-комнату
            self.chat_room = await self.get_chat_room()
            
            # Проверяем, что пользователь участник этого чата
            if not await self.check_user_in_chat():
                print("   ❌ User not in this chat, closing connection")
                await self.close(code=4003)
                return
            
            print(f"   ✅ Chat room ID: {self.chat_room.id}")

            self.room_group_name = f'chat_room_{self.chat_room.id}'
            print(f"   Room group name: {self.room_group_name}")

            # Присоединяемся к группе
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print("   ✅ Added to channel layer group")

            await self.accept()
            print("   ✅ WebSocket connection accepted")

            # Отправляем приветственное сообщение
            await self.send(json.dumps({
                'type': 'system',
                'message': f'Вы подключились к чату',
                'timestamp': 'just now'
            }))

        except Exception as e:
            print(f"   ❌ Error in connect: {e}")
            import traceback
            traceback.print_exc()
            await self.close(code=4000)  # Custom code for general error

    async def disconnect(self, close_code):
        print(f"🔌 WebSocket disconnect, code: {close_code}")
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print("   ✅ Removed from channel layer group")

    async def receive(self, text_data):
        print(f"📨 Received message from {self.user.username}")
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json.get('message', '').strip()

            if not message_content:
                return

            # Сохраняем сообщение
            saved_message = await self.save_message(message_content)

            # Отправляем всем в группе
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': saved_message.id,
                    'sender_id': self.user.id,
                    'sender_username': self.user.username,
                    'content': message_content,
                    'timestamp': saved_message.timestamp.isoformat(),
                }
            )

        except Exception as e:
            print(f"   ❌ Error in receive: {e}")

    async def chat_message(self, event):
        """Отправка сообщения всем подключенным клиентам"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': event['message_id'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'content': event['content'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def get_chat_room(self):
        from .models import ChatRoom
        from django.core.exceptions import ObjectDoesNotExist

        try:
            chat_room = ChatRoom.objects.get(id=self.chat_room_id)
            print(f"   ✅ Found existing chat room: {chat_room.id}")
        except ObjectDoesNotExist:
            print(f"   ⚠️  Chat room #{self.chat_room_id} not found")
            raise Exception(f"Чат-комната #{self.chat_room_id} не найдена")

        return chat_room

    @database_sync_to_async
    def check_user_in_chat(self):
        """Проверяем, что пользователь участник этого чата"""
        is_participant = self.user.id in [self.chat_room.user_id, self.chat_room.owner_id]
        if is_participant:
            print(f"   ✅ User is participant (user_id={self.chat_room.user_id}, owner_id={self.chat_room.owner_id})")
        return is_participant

    @database_sync_to_async
    def save_message(self, content):
        from .models import Message

        message = Message.objects.create(
            chat_room=self.chat_room,
            sender=self.user,
            content=content
        )

        # Обновляем время последнего сообщения в чат-комнате
        self.chat_room.save()  # auto_now=True обновит updated_at

        return message
