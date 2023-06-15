from channels.generic.websocket import AsyncWebsocketConsumer
import html
import json
from channels.db import database_sync_to_async
from .models import Chat

class ChatAssistenza(AsyncWebsocketConsumer):

    @database_sync_to_async
    def termina_chat(self):
        chat = Chat.objects.get(pk=self.scope['url_route']['kwargs']['room'])
        chat.stato = 'terminato'
        chat.save()
    
    async def messaggio_abbandono(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'invio_messaggio',
                'msg': '',
                'iden': '',
                'foto_profilo': '',
                'situazione': 'abbandono'
            }
        )


    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'chat_' + str(self.room_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.messaggio_abbandono()
        await self.termina_chat()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        iden = html.escape(text_data_json['iden'])
        messaggio = html.escape(text_data_json['msg'])
        foto_profilo = html.escape(text_data_json['fotoProfilo'])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'invio_messaggio',
                'msg': messaggio,
                'iden': iden,
                'foto_profilo': foto_profilo,
                'situazione': 'normale'
            }
        )

    async def invio_messaggio(self, event):
        messaggio = event['msg']
        iden = event['iden']
        situazione = event['situazione']
        foto_profilo = event['foto_profilo']

        await self.send(text_data=json.dumps({
            'msg': messaggio,
            'iden': iden,
            'fotoProfilo': foto_profilo,
            'situazione': situazione,
        }))
        
