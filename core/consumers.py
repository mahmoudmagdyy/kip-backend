import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ReservedSlot
from .serializer import ReservedSlotSerializer


class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join admin booking room
        self.room_group_name = 'admin_bookings'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave admin booking room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'get_bookings':
            # Send current bookings to client
            bookings = await self.get_latest_bookings()
            await self.send(text_data=json.dumps({
                'type': 'bookings_data',
                'data': bookings
            }))

    # Receive message from room group
    async def booking_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'booking_update',
            'data': event['data']
        }))

    async def booking_created(self, event):
        # Send new booking to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'booking_created',
            'data': event['data']
        }))

    async def booking_updated(self, event):
        # Send updated booking to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'booking_updated',
            'data': event['data']
        }))

    async def booking_deleted(self, event):
        # Send deleted booking info to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'booking_deleted',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_latest_bookings(self):
        """Get latest bookings with user details"""
        bookings = ReservedSlot.objects.all().order_by('-created_at')[:50]
        bookings_data = []
        
        for booking in bookings:
            booking_dict = ReservedSlotSerializer(booking).data
            
            # Add user details
            user = booking.user
            user_data = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.username,
                "is_active": user.is_active,
                "date_joined": user.date_joined.isoformat() if user.date_joined else None
            }
            
            # Add profile details if exists
            try:
                profile = user.profile
                user_data.update({
                    "gender": profile.gender,
                    "country": profile.country
                })
            except:
                user_data.update({
                    "gender": "",
                    "country": ""
                })
            
            booking_dict['user_details'] = user_data
            bookings_data.append(booking_dict)
        
        return bookings_data
