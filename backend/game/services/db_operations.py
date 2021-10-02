from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from game.models import Room, Player, Fields, Message
from django.core.management import call_command


def get_field_and_add_to_player(player: Player) -> Fields:
    """
    Assign field to player. Creates data if db fields is empty.
    """
    field = Fields.objects.filter(id=1).first()
    if not field:
        call_command('loaddata', 'fields')
        field = Fields.objects.filter(id=1).first()
    field = field.fields if not player.field else player.field
    player.field = field
    player.save()
    return field


def create_empty_room(latest_room: Room) -> Room:
    """
    Creates first room in db or one one after latest_room.
    """
    if not latest_room:
        return Room.objects.create(id=0, name=f'room_{0}')
    else:
        return Room.objects.create(id=latest_room.id + 1, name=f'room_{latest_room.id + 1}')

def get_vacant_room() -> Room:
    """
    Checks if room can accept a new user or its already full.
    """
    last_room = Room.objects.all().order_by('-id').first()
    if last_room:
        if not last_room.first_user or not last_room.second_user:
            return last_room
    return create_empty_room(last_room)

def get_or_create_room(player: Player) -> Room:
    """
    Returns player's prev room or creates new one.
    """
    room = Room.objects.filter(name=player.room).first()
    if room:
        return room
    else:
        return get_vacant_room()  # TODO: message that previous room was ended or not exist.


def room_has_this_player(player) -> bool:
    room = Room.objects.filter(name=player.room).first()
    if player.room and room:
        if room.first_user == player \
                or room.second_user == player:
            return True
        else:
            return False
    else:
        return False


def make_player_offline(player: Player):
    """
    Changes is_in_the_room field of player.
    """
    if player.is_in_the_room:
        player.is_in_the_room = False
        player.save()


def if_room_empty_delete_ref_data(room) -> bool:
    """
    Deletes ref messages and room itself.

    :return: Was deleted or not
    """
    if room:
        try:
            actual_room = Room.objects.get(name=room)
            if not actual_room.first_user.is_in_the_room and not actual_room.second_user.is_in_the_room:
                Message.objects.filter(room_name=actual_room.name).delete()
                actual_room.delete()
                return True
        except (ObjectDoesNotExist, AttributeError) as e:
            return False
    else:
        return False


def fill_the_room(room: Room, player: Player):
    """
    Adds player to room's data if it's not full.
    """
    room_ = Room.objects.get(name=room.name)
    if not room_.first_user:
        room_.first_user = player
        room_.first_field = player.field
    elif room_.first_user and not room_.second_user and (player.username != room_.first_user.username):
        room_.second_user = player
        room_.second_field = player.field
    room_.save()


def add_group_channel_to_the_room(room: Room):
    """
    Adds group if empty.
    """
    if not room.group_channel_name:
        room.group_channel_name = 'group_' + room.name
        room.save()


def fill_player_essentials_to_connect(player: Player, channel_name: str) -> bool:
    """
    Saves new player's data.
    """
    if channel_name:
        player.channel_name = channel_name
        player.is_in_the_room = True
        player.save()
        return True
    else:
        return False


def get_player_or_redirect_to_login(scope):
    """
    Returns player from scope if exist, otherwise redirect.
    """
    user = scope['user']
    player = Player.objects.filter(username=user.username).first()
    if player:
        return player
    else:
        return redirect(
            'login'
        )


def get_player_room_or_new(player: Player, new_room_name: str) -> Room:
    if player.room:
        return Room.objects.get(name=player.room)
    else:
        try:
            return Room.objects.get(name=new_room_name)
        except:
            return Room.objects.create(name=new_room_name)
