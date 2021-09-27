from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from game.models import Player, Room, Message


class MyExceptionMiddleware(object):
    """
    Resets all rooms if there is an exception.
    """
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            Room.objects.all().delete()
            Player.objects.all().delete()
            Message.objects.all().delete()
            return redirect(
                'game_lobby'
            )