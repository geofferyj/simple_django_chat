from django.db import models
from django.utils.translation import gettext as _
import uuid

from users.models import User


class Chat(models.Model):
    """
    Chat model
    """
    id = models.UUIDField(_(""), default=uuid.uuid4, primary_key=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    message = models.TextField(_("Message"))
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='chats')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def to_json(self):
        return {
            'id': str(self.id),
            'sender': self.sender.username,
            'receiver': self.receiver.username,
            'message': self.message,
            'timestamp': self.timestamp.strftime("%d/%m/%Y %H:%M:%S"),
            'room': str(self.room.id),
            'is_read': self.is_read,
            'read_at': self.read_at.strftime('%Y-%m-%d %H:%M:%S') if self.read_at else None
        }
    
    def from_json(self, json_data):
        self.sender = json_data.get('sender')
        self.receiver = json_data.get('receiver')
        self.message = json_data.get('message')
        self.timestamp = json_data.get('timestamp')
        self.room = json_data.get('room')
        self.read = json_data.get('read')
        self.read_at = json_data.get('read_at')


    class Meta:
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")


    def __str__(self):
        return f"from {self.sender.username} to {self.receiver.username}"

class Room(models.Model):
    """
    Room model
    """
    id = models.UUIDField(_(""), default=uuid.uuid4, primary_key=True)
    participants = models.ManyToManyField(User, related_name='rooms')
    name = models.CharField(_("Name"), max_length=100)

    def to_json(self):
        return {
            'id': str(self.id),
            'participants': [p.username for p in self.participants.all()],
            'name': self.name
        }
    
    def get_chats_as_json(self):
        return [c.to_json() for c in self.chats.all()]

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


    def __str__(self):
        return f"{self.name}"