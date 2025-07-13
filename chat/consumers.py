import json
from datetime import timezone
from .models import PrivateMessage
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # دریافت کاربر فعلی از scope
        self.user = self.scope['user']

        # اگر کاربر لاگین نباشد، اتصال را قطع می‌کنیم
        if not self.user.is_authenticated:
            await self.close()
            return

        # ID کاربر جاری را به عنوان نام کانال استفاده می‌کنیم
        self.user_channel_name = f"user_{self.user.id}"

        # کاربر را به گروه خودش اضافه می‌کنیم
        await self.channel_layer.group_add(
            self.user_channel_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, data=None, bytes_data=None):
        try:
            data = json.loads(data)
            receiver_id = data.get('receiver_id')
            message_content = data.get('message')

            if not receiver_id or not message_content:
                await self.send(json.dumps({
                    'error': 'Both receiver_id and message are required'
                }))
                return

            # دریافت کاربر با استفاده از sync_to_async
            receiver = await sync_to_async(User.objects.filter(id=receiver_id).first)()

            if not receiver:
                await self.send(json.dumps({
                    'error': 'Receiver not found'
                }))
                return

            # ذخیره پیام در دیتابیس
            await sync_to_async(PrivateMessage.objects.create)(
                sender=self.user,
                receiver=receiver,
                message=message_content
            )

            # ارسال پیام به دریافت کننده
            await self.channel_layer.group_send(
                f"user_{receiver_id}",
                {
                    'type': 'private_message',
                    'sender_id': self.user.id,
                    'sender_username': self.user.username,
                    'message': message_content,
                    'timestamp': str(timezone.now())
                }
            )

            # تأیید ارسال به فرستنده
            await self.send(json.dumps({
                'status': 'message sent',
                'receiver_id': receiver_id,
                'message': message_content
            }))

        except json.JSONDecodeError:
            await self.send(json.dumps({'error': 'Invalid JSON format'}))
        except Exception as e:
            await self.send(json.dumps({'error': str(e)}))
    async def private_message(self, event):
        # این متد زمانی فراخوانی می‌شود که پیامی برای این کاربر ارسال شده باشد
        await self.send(json.dumps({
            'type': 'private_message',
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def disconnect(self, close_code):
        # حذف کاربر از گروه هنگام قطع ارتباط
        if hasattr(self, 'user_channel_name'):
            await self.channel_layer.group_discard(
                self.user_channel_name,
                self.channel_name
            )