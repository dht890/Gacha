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

    def validate(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Card name must be a non-empty string.")

        if self.rarity not in ["common", "rare", "epic", "legendary"]:
            raise ValueError(f"Invalid rarity: {self.rarity}")

        if not isinstance(self.icon, str):
            raise ValueError("Icon must be a string (e.g., URL or filename).")

        if not isinstance(self.cost, int) or not (1 <= self.cost <= 10):
            raise ValueError("Elixir cost must be an integer between 1 and 10.")
