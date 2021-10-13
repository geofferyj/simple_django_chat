from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response

from chat.models import Room
from chat.serializers import RoomSerializer
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
from core.utils import QSTokenAuthentication



class RoomViewSet(ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned rooms
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Room.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(participants__in=[username])
        return queryset
    
    @action(
        detail=False, 
    methods=['POST', 'PUT'], 
    permission_classes=[IsAuthenticated],
    authentication_classes=[QSTokenAuthentication],)
    def mark_as_read(self, request, *args, **kwargs):
        """
        Mark all messages as read.
        """
        try:
            room_id = request.data.get("room_id")
            room = get_object_or_404(Room, id=room_id)
        except ValidationError:
            return Response(
                {
                    "message": "Invalid Room id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        chats = room.chats.filter(receiver=request.user)
        chats.update(is_read=True, read_at=datetime.now())

        return Response(status=status.HTTP_204_NO_CONTENT)