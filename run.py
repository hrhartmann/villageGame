
from env import Environment
from utils import read_players

players_file = "test.txt"
players = read_players(players_file)
world = Environment(players)
