from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from game.models import Room, Player, Fields, Message


def get_field_and_add_to_player(player) -> Fields:
    field = Fields.objects.get(id=1).fields if not player.field else player.field
    player.field = field
    player.save()
    return field


def get_or_create_room(player) -> Room:
    def get_vacant_room():
        'Checks if room can accept a new user or its already full.'

        def create_empty_room(latest_room):
            if not last_room:
                return Room.objects.create(id=0, name=f'room_{0}')
            else:
                return Room.objects.create(id=latest_room.id + 1, name=f'room_{latest_room.id + 1}')

        last_room = Room.objects.all().order_by('-id').first()
        if last_room:
            if not last_room.first_user or not last_room.second_user:
                return last_room
        return create_empty_room(last_room)

    try:
        return Room.objects.get(name=player.room)
    except ObjectDoesNotExist:
        return get_vacant_room()  # TODO: message that previous room was ended or not exist.


def room_has_this_player(player) -> bool:
    room = Room.objects.filter(name=player.room).first()
    if player.room and room is not None :
        if room.first_user == player \
            or room.second_user == player:
            return True
    else:
        return False


def make_player_offline(player):
    if player.is_in_the_room:
        player.is_in_the_room = False
        player.save()



def if_room_empty_delete_ref_data(room):
    if room is not None:
        try:
            actual_room = Room.objects.get(name=room)
            if not actual_room.first_user.is_in_the_room and not actual_room.second_user.is_in_the_room:
                Message.objects.filter(room_name=actual_room.name).delete()
                actual_room.delete()
        except (ObjectDoesNotExist, AttributeError) as e:
            print(e)


def fill_the_room(room, player):
    room_ = Room.objects.get(name=room.name)
    if not room_.first_user:
        room_.first_user = player
        room_.first_field = player.field
    elif room_.first_user and not room_.second_user and (player.username != room_.first_user.username):
        room_.second_user = player
        room_.second_field = player.field
    room_.save()


def add_group_channel_to_the_room(room):
    if not room.group_channel_name:
        room.group_channel_name = 'group_' + room.name
        room.save()


def fill_player_essentials_to_connect(player, channel_name):
    player.channel_name = channel_name
    player.is_in_the_room = True
    player.save()


def get_player_or_redirect_to_login(scope):
    user = scope['user']
    try:
        return Player.objects.get(username=user.username)
    except ObjectDoesNotExist:
        return redirect(
            'login'
        )


def get_player_room_or_new(player, new_room_name):
    if player.room:
        return Room.objects.get(name=player.room)
    else:
        return Room.objects.get(name=new_room_name)
