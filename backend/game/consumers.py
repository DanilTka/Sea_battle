import json

from django.http import HttpResponse

from game.services import db_operations
from game.services.db_operations import room_has_this_player
from .models import Message, Room

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from game.services.service import array_to_str, to_array


class SeaBattleConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        player_or_redirect = db_operations.get_player_or_redirect_to_login(
            scope=self.scope,
        )

        if player_or_redirect is HttpResponse:
            return player_or_redirect
        else:
            self.player = player_or_redirect

        self.room = db_operations.get_player_room_or_new(
            player=self.player,
            new_room_name=self.room_name
        )

        db_operations.fill_player_essentials_to_connect(
            player=self.player,
            channel_name=self.channel_name
        )

        db_operations.add_group_channel_to_the_room(
            room=self.room,
        )

        self.join_room()

        return self.reconnect() \
            if room_has_this_player(player=self.player) \
            else self.new_connect()

    def new_connect(self):
        self.player.room = self.room_name
        self.player.save()
        db_operations.fill_the_room(
            room=self.room,
            player=self.player
        )
        self.start_game_if_rooms_full()

    def reconnect(self):
        if self.room.whos_turn:
            self.unpause_game()
        else:
            self.start_game_if_rooms_full()

    def join_room(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room.group_channel_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room.group_channel_name,
            self.player.channel_name
        )

    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data_json)

    def group_send_data(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room.group_channel_name,
            {
                'type': 'send_data',
                'message': message
            }
        )

    def group_send_event(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room.group_channel_name,
            {
                'type': 'send_event',
                'message': message
            }
        )

    def channel_send_data(self, message, channel_name):
        async_to_sync(self.channel_layer.send)(
            channel_name,
            {
                'type': 'send_data',
                'message': message
            }
        )

    def send_event(self, message):
        self.send(text_data=json.dumps(message))

    def send_data(self, event):
        self.send(text_data=json.dumps(event['message']))

    def start_game_if_rooms_full(self):
        self.room = Room.objects.get(name=self.room_name)
        if self.room.first_user and self.room.second_user:
            if not self.room.second_field or not self.room.first_field:
                self.room.second_field = self.room.second_user.field
                self.room.first_field = self.room.first_user.field
            self.room.whos_turn = self.room.first_user
            self.room.save()
            self.send_primary_game_data()

    def update_player_field_in_the_room(self, data):
        self.room = Room.objects.get(name=self.room_name)
        value_array = data['rival_field_update_value']
        id_array = data['rival_field_update_id'][1:]
        if data['username'] == self.room.first_user.username:
            array = to_array(self.room.second_field)
            array[int(id_array[0])][int(id_array[1])] = value_array
            self.room.second_field = array_to_str(array)
            self.room.first_count = data['user_count']
        elif data['username'] == self.room.second_user.username:
            array = to_array(self.room.first_field)
            array[int(id_array[0])][int(id_array[1])] = value_array
            self.room.first_field = array_to_str(array)
            self.room.second_count = data['user_count']

        self.room.save()

    def send_primary_game_data(self):
        content_for_first = {
            'command': 'game_created',
            'rival_field': to_array(self.room.second_field),
            'whos_turn': self.room.whos_turn.username,
        }
        self.channel_send_data(content_for_first, self.room.first_user.channel_name)
        content_for_second = {
            'command': 'game_created',
            'rival_field': to_array(self.room.first_field),
            'whos_turn': self.room.whos_turn.username,
        }
        self.channel_send_data(content_for_second, self.room.second_user.channel_name)

    def send_game_state_to(self, data):
        self.room = Room.objects.get(name=self.room_name)

        self.update_player_field_in_the_room(data)

        if data['username'] == self.room.first_user.username:
            content = {
                'command': 'game_state',
                'user_field_update_id': data['rival_field_update_id'],
                'user_field_update_value': data['rival_field_update_value'],
                'rival_count': data['user_count'],
                'whos_turn': self.room.second_user.username
            }
            self.channel_send_data(content, self.room.second_user.channel_name)
        else:
            content = {
                'command': 'game_state',
                'user_field_update_id': data['rival_field_update_id'],
                'user_field_update_value': data['rival_field_update_value'],
                'rival_count': data['user_count'],
                'whos_turn': self.room.first_user.username
            }
            self.channel_send_data(content, self.room.first_user.channel_name)

    def unpause_game(self):
        self.room = Room.objects.get(name=self.room_name)
        if self.player.username == self.room.first_user.username:
            content = {
                'command': 'game_unpause',
                'user_field': to_array(self.room.first_field),
                'rival_field': to_array(self.room.second_field),
                'user_count': self.room.first_count,
                'rival_count': self.room.second_count,
                'whos_turn': self.room.whos_turn.username
            }
        else:
            content = {
                'command': 'game_unpause',
                'user_field': to_array(self.room.second_field),
                'rival_field': to_array(self.room.first_field),
                'user_count': self.room.second_count,
                'rival_count': self.room.first_count,
                'whos_turn': self.room.whos_turn.username
            }
        self.channel_send_data(content, channel_name=self.channel_name)

    def fetch_messages(self, data):
        if data['room_name'] == self.room_name:
            messages = Message.load_messages(data['room_name'])
            content = {
                'command': 'messages',
                'messages': self.messages_to_json(messages),
                'player_id': self.player.username
            }
            self.channel_send_data(content, self.channel_name)

    def new_message(self, data):
        message = Message.objects.create(
            content=data['message'],
            player=self.player.username,
            room_name=self.room_name,
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.group_send_data(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'player': message.player,
            'room_name': message.room_name,
            'content': message.content,
            'timestamp': format(message.timestamp, "%H:%M:%S")
        }

    commands = {
        'send_primary_game_data': send_primary_game_data,
        'send_game_state_to': send_game_state_to,
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }
