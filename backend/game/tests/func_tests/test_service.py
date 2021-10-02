from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.test import TestCase

from game.models import Room, Player
from game.services.service import find_opponent, lobby_actions, to_array, array_to_str


class GameViewsTest(LoginRequiredMixin, TestCase):
    fixtures = ['test_data.json']

    def test_find_opponent(self):
        self.assertTrue(isinstance(find_opponent("find_opponent", Room.objects.filter().first()), HttpResponseRedirect))
        self.assertEqual(find_opponent("find_opponent", None), None)
        self.assertEqual(find_opponent("-------------", Room.objects.filter().first()), None)
        self.assertEqual(find_opponent("-------------", None), None)

    def test_lobby_actions(self):
        self.assertTrue(lobby_actions(['find_opponent'], Player.objects.filter().first()), ('find_opponent', Room.objects.get()))
        self.assertEqual(lobby_actions(['shuffle'], Player.objects.filter().first()), (None, None))
        self.assertEqual(lobby_actions(['shuffle'], None), (None, None))
        self.assertTrue(lobby_actions(['find_opponent'], None), (None, None))
        self.assertEqual(lobby_actions([], Player.objects.filter().first()), (None, None))

    def test_to_array(self):
        matrix = [['0', '1', '1', '1', '1', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
             ['1', '0', '1', '0', '0', '0', '0', '0', '1', '0'],
             ['1', '0', '1', '0', '0', '1', '0', '0', '0', '0'],
             ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0'],
             ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '1', '1', '1', '0', '0', '1', '1', '0', '0']]
        bad_matrix = [['0', '1', '1', '1', '1', '0', '0', '0', '0', '0'],
                      ['0', '0', '0', '0', '0', '0', '0', 'f', 'g', 'h'],
                      ['1', '0', '1', '0', '0', '0', '0', '0', '1', '1'],
                      ['2', '3', '4', '5', '0', '1', '0', '0', '0', '0'],
                      ['0', '0', '1', '0', '0', '0', '0', '0', 't', 'h'],
                      ['m', '0', '0', '0', '0', '0', '1', '0', '0', '0'],
                      ['0', '0', '1', '0', '0', '0', '0', '0', '7', '8'],
                      ['9', '8', '7', '0', '0', '0', '0', '0', '0', '1'],
                      ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                      ['0', '1', '1', '1', '0', '0', '1', '1', '0', '0']]

        with self.assertRaises(IndexError):
            to_array("011110046462626hgf0000256246101000001")
        self.assertTrue(
            to_array("0111100000000000000010100000101010010000001000000000000010000010000000000000000100000000010111001100") == \
            matrix)
        self.assertTrue(to_array(None) == [None])
        self.assertTrue(
            to_array("01111000000000000fgh1010000011234501000000100000thm0000010000010000078987000000100000000010111001100") == \
            bad_matrix)

    def test_array_to_str(self):
        matrix = [['0', '1', '1', '1', '1', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
             ['1', '0', '1', '0', '0', '0', '0', '0', '1', '0'],
             ['1', '0', '1', '0', '0', '1', '0', '0', '0', '0'],
             ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0'],
             ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '1', '1', '1', '0', '0', '1', '1', '0', '0']]
        bad_matrix = [['0', '1', '1', '1', '1', '0', '0', '0', '0', '0'],
                      ['0', '0', '0', '0', '0', '0', '0', 'f', 'g', 'h'],
                      ['1', '0', '1', '0', '0', '0', '0', '0', '1', '1'],
                      ['2', '3', '4', '5', '0', '1', '0', '0', '0', '0'],
                      ['0', '0', '1', '0', '0', '0', '0', '0', 't', 'h'],
                      ['m', '0', '0', '0', '0', '0', '1', '0', '0', '0'],
                      ['0', '0', '1', '0', '0', '0', '0', '0', '7', '8'],
                      ['9', '8', '7', '0', '0', '0', '0', '0', '0', '1'],
                      ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
                      ['0', '1', '1', '1', '0', '0', '1', '1', '0', '0']]
        short_bad_matrix = [['0', '1', '1', '1', '1', '0', '0', '0'],
                      ['0', '0', '0', '0', '0', '0', '0', 'f'],
                      ['1', '0', '1', '0', '0', '0', '0', '0'],
                      ['2', '3', '4', '5', '0', '1', '0', '0'],
                      ['0', '1', '1', '1', '0', '0', '1', '1']]
        self.assertTrue(
            array_to_str(
                matrix) == \
            "0111100000000000000010100000101010010000001000000000000010000010000000000000000100000000010111001100")
        self.assertTrue(array_to_str(None) == "")
        self.assertTrue(
            array_to_str(
                bad_matrix) == \
            "01111000000000000fgh1010000011234501000000100000thm0000010000010000078987000000100000000010111001100")

        self.assertTrue(
            array_to_str(short_bad_matrix) == \
            "011110000000000f101000002345010001110011"
        )
