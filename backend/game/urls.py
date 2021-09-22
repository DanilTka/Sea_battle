from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.game, name='game'),
    path('game/<str:room_name>/', views.game_room, name='game_room'),
]