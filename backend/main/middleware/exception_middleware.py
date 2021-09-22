from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from game.models import Player, Room, Message


class MyExceptionMiddleware(object):
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    def process_exception(self, request, exception):
        print('MyMiddleware')
        if isinstance(exception, ObjectDoesNotExist):
            messages.error(request, 'Something went wrong. The room has been deleted.')
            Room.objects.all().delete()
            Player.objects.all().delete()
            Message.objects.all().delelte()