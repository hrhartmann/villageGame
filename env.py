
import random

from utils import select_option, save_char
from human import Human

class Environment:

    def __init__(self, players, days=0):
        self.players = [Human(name) for name in players]
        self.days = days

    def run(self):
        while self.check_alive_players():
            self.env_day()

    def check_alive_players(self):
        for p in self.players:
            if p.coma == False:
                return True
        return False

    def env_day(self):
        self.days += 1
        print("%%"*25)
        print(f"Day: {self.days }")
        for player in self.players:
            self.day(player)
            save_char(player)

    def day(self, char):
        while char.actions > 0:
            sel, act = char.select_action()
            if sel == "work":
                self.work(char, act)
            elif sel == "sell":
                self.sell(char)
            elif sel == "buy":
                self.buy(char)
        char.sleep()

    def work(self, char, action):
        if action == "farmer":
            self.farmer(char)
        elif action == "architect":
            self.architect(char)
        elif action == "hunter":
            self.hunter(char)
        elif action == "blacksmith":
            self.blacksmith(char)

    def farmer(self, char):
        prob = random.random() * (char.tool_lvl + 1)
        collect = prob
        if char.skills["farmer"] > 3:
            char.food_inv["steak"].quantity += collect
        elif char.skills["farmer"] == 3:
            char.food_inv["eggs"].quantity += collect
        elif char.skills["farmer"] == 2:
            char.food_inv["cereals"].quantity += collect
        elif char.skills["farmer"] == 1:
            char.food_inv["apples"].quantity += collect
        else:
            char.food_inv["berries"].quantity += collect

    def blacksmith(self, char):
        prob = random.random() * (char.home_lvl + 1)
        collect = prob
        if char.skills["blacksmith"] > 3:
            char.items["iron"] += collect
        elif char.skills["blacksmith"] == 3:
            char.items["bronze"] += collect
        elif char.skills["blacksmith"] == 2:
            char.items["stone"] += collect
        elif char.skills["blacksmith"] == 1:
            char.items["wood"] += collect

    def architect(self, char):
        prob = random.random() * (char.tool_lvl + 1)
        if (prob + .4) > 1:
            collect = True
        if collect:
            choose_house = self.choose_house(char)
            char.items[choose_house] += 1

    def choose_house(self, char):
        option = 0
        while option == 0:
            print("Your House options")
            if char.skills["architect"] == 1:
                return "tent"
            elif char.skills["architect"] == 2:
                print("1. tent")
                print("2. hut")
            elif char.skills["architect"] == 3:
                print("3. clay house")
            elif char.skills["architect"] > 3:
                print("4. fort")
            option = select_option(char.skills["architect"])
        if option == 1:
            return "tent"
        elif option == 2:
            return "hut"
        elif option == 3:
            return "clay"
        elif option == 4:
            return "fort"

    def hunter(self, char):
        prob = random.random() * (self.tool_lvl + 1.13)
        collect = prob
        if char.skills["hunter"] > 3:
            char.food_inv["mamut"].quantity += collect
        elif skills["hunter"] == 3:
            char.food_inv["antelope"].quantity += collect
        elif char.skills["hunter"] == 2:
            char.food_inv["wildpig"].quantity += collect
        elif char.skills["hunter"] == 1:
            char.food_inv["rabbit"].quantity += collect

    def sell_item(self, char):
        item = char.select_food(1)
        print("How much? ")
        how_much = select_option(food.quantity)
        price = (food.lvl - 1)*2*how_much
        if price > 0:
            char.sell_food(food, how_much)
            char.get_cash(price)
            return price

    def sell_food(self, char):
        food = char.select_food(1)
        print("How much? ")
        how_much = select_option(food.quantity)
        price = (food.lvl - 1)*2*how_much
        if price > 0:
            char.sell_food(food, how_much)
            char.get_cash(price)
            return price

    def sell(self, char):
        what_to_sell = 0
        while what_to_sell == 0:
            print("1. food")
            print("2. item")
            what_to_sell = select_option(2)
        if what_to_sell == 1:
            self.sell_food(char)
        else:
            self.sell_item(char)

    def buy_food(self, char):
        try:
            foodname = input("Type food name: ")
            foodamount = input("Type quantity: ")
            foodq = float(foodamount)
            char.food_inv[foodname].quantity += foodq
        except Exception as error:
            print(error)

    def buy_item(self, char):
        try:
            iname = input("Type item name: ")
            iamount = input("Type quantity: ")
            q = float(iamount)
            char.items[iname] += q
        except Exception as error:
            print(error)

    def buy(self, char):
        what_to_buy = 0
        while what_to_buy == 0:
            print("1. food")
            print("2. item")
            what_to_buy = select_option(2)
        if what_to_buy == 1:
            self.buy_food(char)
        else:
            self.buy_item(char)
