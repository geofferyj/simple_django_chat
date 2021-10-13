import json
from typing import Optional
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from chat.models import Chat, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # check if user is authenticated
        user = self.scope['user']

        self.user = user

        if user.is_authenticated:
            # get receiver username 
            receiver_username = self.scope['url_route']['kwargs']['username']

            # get receiver
            receiver = await self.get_user(receiver_username)
            self.receiver = receiver

            # if receiver is not found close and return
            if receiver is None:
                await self.send(text_data=json.dumps({
                    'message': 'User not found'
                }))
                
                self.room_group_name = 'chat_default'
                await self.close(3000)
                return

            # check if room exists between user and receiver
            room = await self.get_room(user, receiver)

            if room is None:
                # create room
                room = await self.create_room(user, receiver)
            

            self.room = room
            # set room group name
            self.room_group_name = f'chat_{room.name}'

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # get room messages
            messages = await self.get_messages(room)

            # send room messages
            await self.channel_layer.group_send(
                self.room_group_name,
            
                {
                    'type': 'chat_message',
                    'message': messages
                }
            )
        
        else:
            self.room_group_name = 'chat_default'
            await self.close(code=4000)
        
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # when a message is received
        # save the message in the database then send it to the room
        text_data_json = json.loads(text_data)
        message = await self.save_message(text_data_json)
        
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message))
    
    @database_sync_to_async
    def get_user(self, username: str) -> Optional[User]:
        User = get_user_model()
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_room(self, user: User, receiver: User)-> Optional[Room]:
        try:
            return Room.objects.filter(participants__in=[user, receiver]).first()
        except Room.DoesNotExist:
            return None
    
    @database_sync_to_async
    def create_room(self, user: User, receiver: User) -> Room:
        room = Room()
        room.name = f'{user.username}_{receiver.username}'
        room.save()
        room.participants.add(user, receiver)
        room.save()
        return room
    
    @database_sync_to_async
    def get_messages(self, room: Room) -> list:
        return room.get_chats_as_json()
    
    @database_sync_to_async
    def save_message(self, text_data_json: dict) -> dict:
        chat = Chat()
        chat.room = self.room
        chat.sender = self.user
        chat.receiver = self.receiver
        chat.message = text_data_json['message']
        chat.save()
        return chat.to_json()
