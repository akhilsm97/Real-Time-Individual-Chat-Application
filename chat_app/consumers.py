import json

from accounts.models import CustomUser
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_app.models import Message
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time chat between two users.

    Responsibilities:
        - Accept and close WebSocket connections.
        - Send and receive chat messages.
        - Handle online status and last seen timestamps.
        - Indicate messages as delivered or read.
        - Notify users of delivery and read receipts.

    Attributes:
        user (CustomUser): The currently connected user.
        other_user_id (int): ID of the user this client is chatting with.
        room_group_name (str): Unique identifier for the chat room.
    """

    async def connect(self):
        """
        Handle a new WebSocket connection.

        - Rejects connection if the user is anonymous.
        - Determines the chat room name based on user IDs.
        - Adds the channel to the group.
        - Marks the current user as online.
        - Marks undelivered messages as delivered and notifies the sender.
        """
        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.other_user_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        users = sorted([self.user.id, self.other_user_id])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # mark user online
        await self.set_online(True)

        # mark old messages delivered
        delivered_ids = await self.mark_delivered()

        for msg_id in delivered_ids:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "delivered_event", "message_id": msg_id}
            )

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        - Removes the channel from the chat group.
        - Marks the current user as offline.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await self.set_online(False)

    async def receive(self, text_data):
        """
        Handle messages received from the WebSocket.

        - Parses the incoming JSON message.
        - Validates that the message is not empty.
        - Creates a Message object in the database.
        - Sends the message to the chat group.
        - Checks if the receiver is online to mark as delivered.

        Args:
            text_data (str): JSON string containing the message data.
        """
        data = json.loads(text_data)
        message_text = data.get("message", "").strip()

        if not message_text:
            return

        receiver = await database_sync_to_async(CustomUser.objects.get)(
            id=self.other_user_id
        )

        # check if receiver online
        delivered = receiver.is_online

        msg = await database_sync_to_async(Message.objects.create)(
            sender=self.user,
            receiver=receiver,
            message=message_text,
            is_delivered=delivered,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "message_event",
                "message": msg.message,
                "sender_id": self.user.id,
                "message_id": msg.id,
                "timestamp": msg.timestamp.strftime("%H:%M"),
                "is_delivered": delivered,
            },
        )

    async def message_event(self, event):
        """
        Send a chat message event to the WebSocket.
        Sends message content, sender info, timestamp, and delivery status.
        Marks message as read if the receiver is the current user.

        Args:
        event (dict): Event data containing message details.
        """
        await self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": event["message"],
                    "sender_id": event["sender_id"],
                    "message_id": event["message_id"],
                    "timestamp": event["timestamp"],
                    "is_delivered": event["is_delivered"],
                }
            )
        )

        # If receiver got message -> mark read
        if self.user.id != event["sender_id"]:
            await self.mark_read(event["message_id"])

    async def delivered_event(self, event):
        """
        Send a message delivered event to the WebSocket.

        Args:
            event (dict): Event data containing the message ID.
        """
        await self.send(
            text_data=json.dumps(
                {"type": "delivered", "message_id": event["message_id"]}
            )
        )

    async def read_event(self, event):
        """
        Send a message read event to the WebSocket.

        Args:
            event (dict): Event data containing the message ID.
        """
        await self.send(
            text_data=json.dumps({"type": "read", "message_id": event["message_id"]})
        )

    @database_sync_to_async
    def set_online(self, status):
        """
        Set the online status and last seen timestamp for the current user.

        Args:
            status (bool): True if the user is online, False otherwise.
        """
        CustomUser.objects.filter(id=self.user.id).update(
            is_online=status, last_seen=now()
        )

    @database_sync_to_async
    def mark_delivered(self):
        """
        Mark all undelivered messages from the other user as delivered.

        Returns:
            list[int]: List of message IDs that were marked as delivered.
        """
        msgs = Message.objects.filter(
            sender_id=self.other_user_id, receiver=self.user, is_delivered=False
        )
        ids = list(msgs.values_list("id", flat=True))
        msgs.update(is_delivered=True)
        return ids

    async def mark_read(self, message_id):
        """
        Mark a specific message as read and notify the chat group.

        Args:
            message_id (int): ID of the message to mark as read.
        """

        await database_sync_to_async(Message.objects.filter(id=message_id).update)(
            is_read=True
        )

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "read_event", "message_id": message_id}
        )
