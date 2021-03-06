
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
        self.coins = 10.0
        self.actions = 2
        self.home_lvl = 0
        self.tool_lvl = 0
        self.food = 3
        self.hungry = False
        self.coma = False

    def __str__(self):
        txtdata = f"name: {self.name} \n"
        txtdata += f"coins: {self.coins} \n"
        txtdata += f"actions: {self.actions} \n"
        txtdata += f"food: {self.food} \n"
        txtdata += f"home_lvl: {self.home_lvl} \n"
        txtdata += f"tool_lvl: {self.tool_lvl} \n"
        if self.hungry:
            txtdata += "Hungry!!"
        if self.coma:
            txtdata += "In coma ????"
        return txtdata

    def get_full_data(self):
        data = str(self)
        data += str("###") + "\n"
        data += self.show_food(show=False) + "\n"
        data += str(self.skills) + "\n"
        data += str(self.items) + "\n"
        return data


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

    def select_item(self):
        self.show_items()
        choose_item = ""
        item_options = []
        while choose_item == "":
            for item in self.items.keys():
                val = self.items[item]
                if val > 0:
                    item_options.append(item)
            r = input("type food name: ")
            if item_options:
                if r in item_options:
                    choose_item = r
        return self.food_inv[choose_food]

    def sell_food(self, food, q):
        self.food_inv[food.name].drop(q)

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
        if check_balance >= 0:
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
            extra_actions = min([self.food, self.home_lvl])
            self.food -= extra_actions*.8
            self.actions += extra_actions

        elif self.food <= 0:
            self.eat(all=True)
            if self.hungry:
                self.food -= 1
                self.actions = 0
                if self.food < -5:
                    self.coma = True
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
        options_cap = 7
        print("Action options: ")
        print("1. work")
        print("2. sell")
        print("3. eat")
        print("4. level up skill")
        print("5. set home")
        print("6. set tool")
        print("7. buy")

        action = 0
        while self.actions > 0:
            action = select_option(options_cap)
            if action == 1:
                work = self.select_work()
                self.actions -= 1
                return "work", work
            elif action == 2:
                self.actions -= 1
                return "sell", None
            elif action == 3:
                eat_all = False
                r = input("all? (y)")
                if r == "y":
                    eat_all=True
                self.eat(all=eat_all)
                return None, None
            elif action == 4:
                self.actions -= 1
                skill = self.select_work(work_cap=-1)
                level_up(self, skill)
                return None, None
            elif action == 5:
                self.set_home()
                return None, None
            elif action == 6:
                self.set_tool()
                return None, None
            elif action == 7:
                return "buy", None
            return None, None


    def show_food(self, show=True):
        if show:
            print("Food: ")
        food_data = ""
        for food in self.food_inv.values():
            if food.quantity > 0:
                food_data += str(food) + "\n"
                if show:
                    print(food)
        return food_data

    def show_items(self):
        print("Items: ")
        for item in self.items:
            q = self.items[item]
            if q:
                print(item, q)

    def show_skills(self):
        print("Skills:")
        for skill in self.skills:
            skill_lvl = self.skills[skill]
            if skill_lvl > 0:
                print(f"{skill}: {skill_lvl}")

    def show(self):
        print()
        print("##"*25)
        print(self)
        self.show_skills()
        self.show_food()
        self.show_items()

if __name__ == "__main__":
    player = Human("Hans")
    player.coins += 100
    player.select_action()
    player = Human("Rena")
    player.select_action()











































            # Nothing By AbyssalBit ~With Style





































            # Nothing By AbyssalBit ~With Style
