class Chest:
    def __init__(self, chest_type, drop_rate, card_distribution):
        self.type = chest_type
        self.drop_rate = drop_rate
        self.contents = {
            "cards": {
                "distribution": card_distribution
            }
        }

    def to_dict(self):
        return {
            "type": self.type,
            "dropRate": self.drop_rate,
            "contents": self.contents
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            chest_type=data["type"],
            drop_rate=data["dropRate"],
            card_distribution=data["contents"]["cards"]["distribution"]
        ) 