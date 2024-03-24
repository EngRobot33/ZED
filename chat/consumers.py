from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json

class ChattingConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        return await super().connect()
    

    async def receive(self, text_data=None, bytes_data=None):
        return await super().receive(text_data, bytes_data)
    
    async def chat_message(self, event):
        message = event["info"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"data": message}))