import random

from django.shortcuts import redirect

from game.models import Fields
from game.services.db_operations import get_or_create_room


def find_opponent(method, room):
    """
    It handles find_opponent button's action.

    :return: None or redirect to room
    """
    if room and method == 'find_opponent':
        return redirect(
            'game_room', room_name=room.name
        )
    return None


def lobby_actions(POST, player) -> tuple:
    """
    :return: If action is shuffle then second arg is None. If it's find_opponent then room_name.
    """
    if 'shuffle' in POST and player:
        player.field = Fields.objects.get(pk=random.randint(1, 5)).fields
        player.save()
        return None, None

    if 'find_opponent' in POST and player:
        room = get_or_create_room(player=player)
        return 'find_opponent', room
    else:
        return (None, None)


def to_array(field) -> list:
    """
    Converts str representation of field to array.
    0 - empty, 1 - sheep, 2 - shot, 3 - missed.

    :return: 2 dim array.
    """
    if not field:
        return [None]
    matrix = [[0 for x in range(10)] for y in range(10)]
    p = 0
    for i in range(10):
        for j in range(10):
            matrix[i][j] = field[p]
            p += 1
    return matrix


def array_to_str(array: list) -> str:
    """
    Converts 2 dim array to str representations.
    0 - empty, 1 - sheep, 2 - shot, 3 - missed.
    """
    if not array:
        return ""
    string = ''
    for i in range(len(array)):
        for j in range(len(array[i])):
            string += array[i][j]
    return string
