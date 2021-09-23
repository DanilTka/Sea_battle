import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from game.models import Player
from django.utils.safestring import mark_safe
from game.services.service import to_array, find_opponent, \
    lobby_actions
from game.services import db_operations


@login_required
def game(request):
    'Render game lobby'
    player = Player.objects.get_or_create(username=request.user.username)[0]
    db_operations.make_player_offline(player)
    db_operations.if_room_empty_delete_ref_data(room=player.room)
    POST_and_args = lobby_actions(request.POST, player)  # shuffle and find_opponent
    field = db_operations.get_field_and_add_to_player(player)
    redirect_or_none = find_opponent(POST_and_args)
    if redirect_or_none:
        return redirect_or_none

    context = {
        'user_field': mark_safe(json.dumps(to_array(field))),
    }
    return render(request, 'game/game.html', context)


@login_required
def game_room(request, room_name):
    'Render game room with 2 players.'
    context = {
        'room_name': mark_safe(json.dumps(room_name)),
        'user_field': mark_safe(json.dumps(to_array(Player.objects.get(username=request.user).field))),
    }
    return render(request, 'game/game_room.html', context)
