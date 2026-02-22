# models.py
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    """
        Represents a chat message between two users.

        Attributes:
            sender (ForeignKey): The user who sent the message.
            receiver (ForeignKey): The user who receives the message.
            message (TextField): The text content of the message.
            timestamp (DateTimeField): The datetime when the message was created.
            is_delivered (BooleanField): True if the message has been delivered to the receiver.
            is_read (BooleanField): True if the receiver has read the message.
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        """
            Generate a user-friendly string that represents the user.

            Format: "<sender> -> <receiver>"
        """
        return f"{self.sender} -> {self.receiver}"
