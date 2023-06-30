from channels.generic.websocket import AsyncWebsocketConsumer
import html
import json
from channels.db import database_sync_to_async
from .models import Chat

class ChatAssistenza(AsyncWebsocketConsumer):
    """ Implementa il consumer per la chat di assistenza """

    @database_sync_to_async
    def termina_chat(self):
        """ Recupera la chat che corrisponde al numero di stanza nell'url e setta 
        il suo stato a 'terminato' """

        chat = Chat.objects.get(pk=self.scope['url_route']['kwargs']['room'])
        chat.stato = 'terminato'
        chat.save()
    
    async def messaggio_abbandono(self):
        """ Manda un messaggio di abbandono all'altro utente della chat """

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
        """ Crea la connessione dell'utente con il gruppo della chat usando il 
        numero della stanza nell'url """

        self.room_id = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'chat_' + str(self.room_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """ Disconette l'utente dal gruppo della chat ma prima di farlo manda 
        all'altro utente un messaggio di abbandono e cambia lo stato della chat"""

        await self.messaggio_abbandono()
        await self.termina_chat()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """ Implementa la ricezione dei messaggi e il conseguente invio agli 
        altri membri del gruppo"""

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
        """ Invio di un messaggio come JSON """
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
        
