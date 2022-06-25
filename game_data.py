
class Food:

    def __init__(self, name, lvl, foodtype):
        self.name = name
        self.lvl = lvl
        self.foodtype = foodtype
        self.quantity = 0

    def get(self, x):
        self.quantity += x

    def eat(self, x):
        return self.quantity*self.lvl

    def drop(self, x):
        if x >= self.quantity:
            self.quantity -= x

    def reset(self, x):
        self.quantity = 0

    def __str__(self):
        return f"{self.name} lvl {self.lvl} quantity {self.quantity}"


FOOD = {
    "berries": Food("berries", .5, "farmer"),
    "apples": Food("apple", 1, "farmer"),
    "cereals": Food("cereals", 2, "farmer"),
    "eggs": Food("eggs", 3, "farmer"),
    "steak": Food("steak", 4, "farmer"),
    "rabbit": Food("rabbit", 1.5, "hunter"),
    "wildpig": Food("wildpig", 2.5, "hunter"),
    "antelope": Food("antelope", 3.5, "hunter"),
    "mamut": Food("mamut", 5, "hunter"),
}

SKILLS = {
    "farmer": 0,
    "architect": 0,
    "hunter": 0,
    "blacksmith": 0
}

ITEMS = {
    "tent": 0,
    "hut": 0,
    "clay": 0,
    "fort": 0,
    "wood": 0,
    "stone": 0,
    "bronze": 0,
    "iron": 0
}

HOMES = {"tent":1, "hut":2, "clay":3, "fort":4}

TOOLS = {"tent":1, "hut":2, "clay":3, "fort":4}
