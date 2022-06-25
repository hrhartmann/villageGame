
import random

from utils import select_option


class Environment:

    def __init__(self, players):
        self.players = players

    def env_day(self):
        for player in self.players:
            self.day(player)

    def day(self, char):
        char.select_action()



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
        prob = random.random() * (self.tool_lvl + 1)
        collect = prob
        if self.char.skills["farmer"] > 3:
            self.char.food_inv["steak"].quantity += collect
        elif self.char.skills["farmer"] == 3:
            self.char.food_inv["eggs"].quantity += collect
        elif self.char.skills["farmer"] == 2:
            self.char.food_inv["cereals"].quantity += collect
        elif self.char.skills["farmer"] == 1:
            self.char.food_inv["apples"].quantity += collect
        else:
            self.char.food_inv["berries"].quantity += collect

    def blacksmith(self, char):
        prob = random.random() * (self.home_lvl + 1)
        collect = prob
        if self.char.skills["blacksmith"] > 3:
            self.char.items["iron"] += collect
        elif self.char.skills["blacksmith"] == 3:
            self.char.items["bronze"] += collect
        elif self.char.skills["blacksmith"] == 2:
            self.char.items["stone"] += collect
        elif self.char.skills["blacksmith"] == 1:
            self.char.items["wood"] += collect

    def architect(self, char):
        prob = random.random() * (self.tool_lvl + 1)
        if (prob + .4) > 1:
            collect = True
        if collect:
            choose_house = self.choose_house(char)
            self.char.items[choose_house] += 1

    def choose_house(self, char):
        option = 0
        while option == 0:
            print("Your House options")
            if self.char.skills["architect"] == 1:
                return "tent"
            elif self.char.skills["architect"] == 2:
                print("1. tent")
                print("2. hut")
            elif self.char.skills["architect"] == 3:
                print("3. clay house")
            elif self.char.skills["architect"] > 3:
                print("4. fort")
            option = select_option(self.char.skills["architect"])
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
        if self.char.skills["hunter"] > 3:
            self.char.food_inv["mamut"].quantity += collect
        elif self.char.skills["hunter"] == 3:
            self.char.food_inv["antelope"].quantity += collect
        elif self.char.skills["hunter"] == 2:
            self.char.food_inv["wildpig"].quantity += collect
        elif self.char.skills["hunter"] == 1:
            self.char.food_inv["rabbit"].quantity += collect

    def sell_item(self, char):
        pass

    def sell_food(self, char):
        choose_food = ""
        food_options = []
        while choose_food == "":
            for food in char.food_inv:
                if food.quantity > 1:
                    food_options.append(food.name)
                    print(food)
            r = input("type food name: ")
            if food_options:
                if r in food_options:
                    choose_food = r
        return choose_food

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
