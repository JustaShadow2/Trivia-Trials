import unittest
from queryManager import *

# generate and insert a sample game
game = {
    "game_id": 2,
    "level_number": 3,
    "player_index": 5,
    "players": [
        {
        "name": "Player4",
        "password": "password123",
        "streak": 2,
        "duck_count": 0,
        "score": 250
        }
    ]
    }

insert_game(game)

class TestQueryManager(unittest.TestCase):
    def test_dataTypes(self):
        # Test that the data types of the returned values are correct
        self.assertEqual(type(find_game_by_id(2)), dict)
        self.assertEqual(type(get_player_scores()), dict)
        self.assertEqual(type(get_player_info()), dict)

    def test_find_game_by_id(self):
        # Test that the correct game is returned
        self.assertEqual(find_game_by_id(2), game)   


'''
Dont need to test for different data types because these functions are never directly accessed. In order for an incorrect data type to even attempt to be passed, it would have to go through the Board.py file which is impossible.
'''     