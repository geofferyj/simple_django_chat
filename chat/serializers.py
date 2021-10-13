from rest_framework import serializers
from .models import Chat, Room

from users.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for chat object
    """

    class Meta:
      
        model = Chat
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for room object
    """
    chats = ChatSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    
    class Meta:
        
        model = Room
        fields = '__all__'