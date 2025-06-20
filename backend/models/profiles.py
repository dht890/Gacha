class Profile:
    def __init__(self, id, username, xp_lvl=1, pfp=None):
        self.id = id  # This will be unique
        self.username = username  # This will also be unique
        self.xp_lvl = xp_lvl
        self.pfp = pfp

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "xp_lvl": self.xp_lvl,
            "pfp": self.pfp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            username=data["username"],
            xp_lvl=data.get("xp_lvl", 1),
            pfp=data.get("pfp")
        )

    @staticmethod
    def create_indexes(db):
        """Create unique indexes for the profile collection"""
        db.get_collection('profiles').create_index('id', unique=True)
        db.get_collection('profiles').create_index('username', unique=True) 