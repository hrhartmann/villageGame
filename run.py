
from env import Environment
from utils import (
    read_players,
    save_char,
    load_char
)

players_file = "test.txt"
players = read_players(players_file)
world = Environment(players)
save_char(world.players[0])
# world.players[0].save_char
# world.env_day()
