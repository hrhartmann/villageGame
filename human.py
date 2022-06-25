
from utils import (
    select_option,
    select_open_option
)
from game_data import (
    FOOD,
    SKILLS,
    ITEMS,
    HOMES,
    TOOLS
)

SKILLS_REQS = {
    "farmer": {1: ("tool_lvl", 1),
               2: ("home_lvl", 2),
               3: ("home_lvl", 3)},
    "architect": {},
    "hunter": {1: ("tool_lvl", 2),
               3: ("tool_lvl", 3),
               4: ("tool_lvl", 4)},
    "blacksmith": {2: ("home_lvl", 1),
                   3: ("home_lvl", 3)}
}

def check_lvl_up_reqs(char, req, lvlreq):
    if req == "tool_lvl":
        if char.tool_lvl >= lvlreq:
            return True
    elif req == "home_lvl":
        if char.home_lvl >= lvlreq:
            return True
    print(f"{char.name} {req} insufficient")
    return False


def level_up(char, skill, skill_reqs=SKILLS_REQS):
    next_lvl = char.skills[skill] + 1
    cost = next_lvl*10
    if char.get_cash(-cost):
        if next_lvl in skill_reqs[skill].keys():
            req, lvlreq = skill_reqs[skill][next_lvl]
            if check_lvl_up_reqs(char, req, lvlreq):
                char.upgrade_skill(skill)
                return True
        else:
            char.upgrade_skill(skill)
            return True
    else:
        print(f"insufficient cash")
    return False


class Human:

    def __init__(self, name):

        self.name = name
        self.skills = SKILLS
        self.food_inv = FOOD
        self.items = ITEMS
        self.coins = 5.0
        self.actions = 2
        self.home_lvl = 0
        self.tool_lvl = 0
        self.food = 0
        self.hungry = False

    def __str__(self):
        txtdata = f"name: {self.name} \n"
        txtdata += f"coins: {self.coins} \n"
        txtdata += f"actions: {self.actions} \n"
        txtdata += f"food: {self.food} \n"
        txtdata += f"home_lvl: {self.home_lvl} \n"
        txtdata += f"tool_lvl: {self.tool_lvl} \n"
        if self.hungry:
            txtdata += f"Hungry!!"
        return txtdata

    def eat(self, all=False):
        if self.any_food():
            if all:
                for food in self.food_inv.values():
                    self.food += food.eat(food.quantity)
            else:
                satisfied = False
                while not satisfied:
                    r = input("Eat (y): ")
                    if r.lower() == "y":
                        ch_food = self.select_food(0)
                        how_much = select_option(ch_food.quantity)
                        self.food += food.eat(how_much)
                    else:
                        satisfied = False


    def any_food(self):
        for food in self.food_inv.values():
            if food.quantity > .5:
                return True
        return False

    def select_food(self, food_cap):
        self.show_food()
        choose_food = ""
        food_options = []
        while choose_food == "":
            for food in self.food_inv.values():
                if food.quantity > food_cap:
                    food_options.append(food.name)
            r = input("type food name: ")
            if food_options:
                if r in food_options:
                    choose_food = r
        return self.food_inv[choose_food]

    def set_home(self):
        h = select_open_option(HOMES.keys())
        if self.items[h]:
            print(f"Home set to: {h}")
            self.home_lvl = HOMES[h]

    def set_tool(self):
        h = select_open_option(TOOLS.keys())
        if self.items[h]:
            print(f"Tool set to: {h}")
            self.tool_lvl = TOOLS[h]


    def upgrade_skill(self, skill, show=True):
        self.skills[skill] += 1
        if show:
            print(f"{self.name} leveled up in {skill} to {self.skills[skill]}")

    def get_cash(self, x, show=True):
        check_balance = self.coins + x
        if check_balance > 0:
            self.coins += x
            if show:
                print(f"{self.name} got {x}, new balance: {self.coins}")
            return True
        else:
            if show:
                print(f"{self.name} can't get item of price {x}, not enough coins ({self.coins})")
            return False

    def sleep(self):
        if self.food > 0:
            self.food -= 1
            self.actions = 1
            self.actions += max([self.food, self.home_lvl])
        elif self.food == 0:
            self.eat(all=True)
            if self.hungry:
                self.food -= 1
                self.actions = 0
                if self.food < -5:
                    print(f"{self.name} is in coma")
            else:
                self.hungry = True


    def select_work(self, work_cap=0):
        option = 0
        print("Select human option: ")
        while option == 0:
            print("1. farmer")
            if self.skills["architect"] > work_cap:
                print("2. architect")
            if self.skills["hunter"] > work_cap:
                print("3. hunter")
            if self.skills["blacksmith"] > work_cap:
                print("4. blacksmith")
            option = select_option(4)
        if option == 1:
            return "farmer"
        elif option == 2:
            return "architect"
        elif option == 3:
            return "hunter"
        elif option == 4:
            return "blacksmith"

    def select_action(self):
        self.show()
        options_cap = 5
        print("Action options: ")
        print("1. work")
        print("2. sell")
        print("3. eat")
        print("4. level up skill")
        print("5. set home")
        print("6. sleep")
        print("7. sleep")
        action = 0
        while self.actions > 0:
            action = select_option(options_cap)

        if action == 1:
            work = self.select_work()
            self.actions -= 1
            return "work", work
        elif action == 2:
            self.actions -= 1
            return "sell"
        elif action == 3:
            eat_all = False
            r = input("all? (y)")
            if r == "y":
                eat_all=True
            return self.eat(all=eat_all)
        elif action == 4:
            self.actions -= 1
            skill = self.select_work(work_cap=-1)
            level_up(self, skill)
            return "sell"
        elif action == 5:
            return "sell"
        elif action == 6:
            return "sell"


    def show_food(self):
        print("Food: ")
        for food in self.food_inv.values():
            if food.quantity > 0:
                print(food)

    def show_items(self):
        print("Items: ")
        for item in self.items:
            q = self.items[item]
            if q:
                print(item, q)

    def show(self):
        print()
        print("##"*25)
        print(self)
        self.show_food()
        self.show_items()













































            # Nothing By AbyssalBit ~With Style



if __name__ == "__main__":
    player = Human("Hans")
    player.coins += 100
    player.select_action()
    player = Human("Rena")
    player.select_action()

































            # Nothing By AbyssalBit ~With Style
