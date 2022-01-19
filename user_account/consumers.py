import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name='default_preguntas'
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_group_name)
        # Join room group
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # este cierre solo se hace si se cierra la ventana
        # no si se apaga el server o hay error de server
        print("==========<zx<zx")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        speaker = text_data_json['speaker']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
                 'speaker': speaker
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['text']
        speaker = event['speaker']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': message,
            'speaker': speaker
        }))