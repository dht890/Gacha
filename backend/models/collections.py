class UserCollection:
    def __init__(self, card_id, unlocked=False, level=0, copies_owned=0):
        self.card_id = card_id
        self.unlocked = unlocked
        self.level = level
        self.copies_owned = copies_owned

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "unlocked": self.unlocked,
            "level": self.level,
            "copiesOwned": self.copies_owned
        }
