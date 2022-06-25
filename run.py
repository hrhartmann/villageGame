
from env import Environment
from utils import (
    read_players,
    save_char,
    load_char
)

# players_file = "test.txt"
players_file = "shorttest.txt"
players = read_players(players_file)
world = Environment(players)

world.run()
