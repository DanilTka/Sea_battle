from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import TestCase

from game.models import Player, Fields, Room
from game.services.db_operations import get_field_and_add_to_player, create_empty_room, get_vacant_room, \
    get_or_create_room, room_has_this_player, make_player_offline, if_room_empty_delete_ref_data, fill_the_room, \
    add_group_channel_to_the_room, fill_player_essentials_to_connect, get_player_or_redirect_to_login, \
    get_player_room_or_new


class GameViewsTest(LoginRequiredMixin, TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.pl = Player.objects.filter().first()
        self.room = Room.objects.filter().first()
        self.pl2 = Player.objects.create(username="123")



    def test_get_field_and_add_to_player(self):
        player = Player.objects.create(
            username="123",
            field="0100000000000111100000000000011000000000101100001110000000000010000000000010010000001000001110000000"
        )
        self.assertEqual(
            get_field_and_add_to_player(player),
            Fields.objects.get(id=3).fields)

        player2 = Player.objects.create(
            username="123"
        )
        self.assertEqual(
            get_field_and_add_to_player(player2),
            Fields.objects.get(id=1).fields)

        Fields.objects.all().delete()
        self.assertEqual(
            get_field_and_add_to_player(player2),
            Fields.objects.get(id=1).fields)

    def test_create_empty_room(self):
        self.assertEqual(
            create_empty_room(Room.objects.order_by("-pk").filter().first()),
            Room.objects.order_by("-pk").filter().first())

        self.assertEqual(
            create_empty_room(None),
            Room.objects.filter(id=0).first())

    def test_get_vacant_room(self):
        self.assertEqual(
            get_vacant_room(),
            Room.objects.all().order_by('-id').first())
        Room.objects.all().delete()
        self.assertEqual(
            get_vacant_room(),
            Room.objects.get(id=0))

    def test_get_or_create_room(self):
        self.assertEqual(
            get_or_create_room(self.pl),
            get_vacant_room()
        )
        self.pl.room = 'room_test'
        pl_room = Room.objects.get(name='room_test')
        self.pl.save()
        self.assertEqual(
            get_or_create_room(self.pl),
            pl_room
        )

    def test_room_has_this_player(self):
        self.assertEqual(
            room_has_this_player(self.pl),
            False
        )
        self.pl.room = 'room_test'
        self.pl.save()
        self.assertEqual(
            room_has_this_player(self.pl),
            False
        )
        room = Room.objects.get(name='room_test')
        room.first_user = self.pl
        room.save()
        self.assertEqual(
            room_has_this_player(self.pl),
            True
        )
        Room.objects.all().delete()
        self.assertEqual(
            room_has_this_player(self.pl),
            False
        )

    def test_make_player_offline(self):
        make_player_offline(self.pl)
        self.assertEqual(
            self.pl.is_in_the_room,
            False
        )
        self.pl.is_in_the_room = True
        self.pl.save()
        make_player_offline(self.pl)
        self.assertEqual(
            self.pl.is_in_the_room,
            False
        )

    def test_if_room_empty_delete_ref_data(self):
        self.assertEqual(
            if_room_empty_delete_ref_data(self.room.name),
            False
        )

        self.room.first_user = self.pl
        self.room.second_user = self.pl2
        self.room.save()
        self.assertEqual(
            if_room_empty_delete_ref_data(self.room.name),
            True
        )

        self.assertEqual(
            if_room_empty_delete_ref_data("room_not_exists"),
            False
        )

    def test_fill_the_room(self):
        fill_the_room(player=self.pl, room=self.room)
        self.room = Room.objects.get(name=self.room.name)
        self.assertTrue(self.room.first_user == self.pl)
        self.assertTrue(self.room.second_user != self.pl)
        fill_the_room(player=self.pl, room=self.room)
        self.room = Room.objects.get(name=self.room.name)
        self.assertTrue(self.room.first_user == self.pl)
        self.assertTrue(self.room.second_user != self.pl)
        fill_the_room(player=self.pl2, room=self.room)
        self.room = Room.objects.get(name=self.room.name)
        self.assertTrue(self.room.first_user == self.pl)
        self.assertTrue(self.room.second_user == self.pl2)

    def test_add_group_channel_to_the_room(self):
        self.assertTrue(
            self.room.group_channel_name == None
        )
        add_group_channel_to_the_room(self.room)
        self.assertTrue(
            self.room.group_channel_name == 'group_'+self.room.name
        )
        add_group_channel_to_the_room(self.room)
        self.assertTrue(
            self.room.group_channel_name == 'group_'+self.room.name
        )

    def test_fill_player_essentials_to_connect(self):
        fill_player_essentials_to_connect(self.pl, None)
        self.assertTrue(self.pl.channel_name == None)
        fill_player_essentials_to_connect(self.pl, '')
        self.assertTrue(self.pl.channel_name == None)
        fill_player_essentials_to_connect(self.pl, 's4df36sd155e6745r746gf4h5dg7st5f76gs')
        self.assertTrue(self.pl.channel_name == 's4df36sd155e6745r746gf4h5dg7st5f76gs')

    def test_get_player_or_redirect_to_login(self):
        scope = {
            'user': self.pl
        }
        self.assertEqual(
            get_player_or_redirect_to_login(scope),
            self.pl
        )
        self.pl = AnonymousUser
        scope = {
            'user': self.pl
        }
        self.assertTrue(isinstance(get_player_or_redirect_to_login(scope), HttpResponseRedirect))

    def test_get_player_room_or_new(self):
        self.assertEqual(
            get_player_room_or_new(self.pl, self.room.name),
            self.room
        )
        self.pl.room = self.room.name
        self.pl.save()
        self.assertEqual(
            get_player_room_or_new(self.pl, self.room.name),
            Room.objects.get(name=self.pl.room)
        )
        self.pl.room = None
        self.assertEqual(
            get_player_room_or_new(self.pl, "room_not_exists"),
            Room.objects.get(name="room_not_exists")
        )
