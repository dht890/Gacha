class Card:
    def __init__(self, name, rarity, icon, cost):
        self.name = name
        self.rarity = rarity
        self.icon = icon
        self.cost = cost

    def to_dict(self):
        return {
            "name": self.name,
            "rarity": self.rarity,
            "icon": self.icon,
            "cost": self.cost
        }
