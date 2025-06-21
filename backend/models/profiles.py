class Profile:
    def __init__(self, username, xp_lvl=1, pfp=None):
        self.username = username  # This will also be unique
        self.xp_lvl = xp_lvl
        self.pfp = pfp

    def to_dict(self):
        return {
            "username": self.username,
            "xp_lvl": self.xp_lvl,
            "pfp": self.pfp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"],
            xp_lvl=data.get("xp_lvl", 1),
            pfp=data.get("pfp")
        )

    @staticmethod
    def create_indexes(db):
        """Create unique indexes for the profile collection"""
        db.get_collection('profiles').create_index('username', unique=True) 

    def validate(self):
        
        if not isinstance(self.username, str) or not self.username:
            raise ValueError("Username must be a non-empty string.")
        
        if not isinstance(self.xp_lvl, int) or self.xp_lvl < 1:
            raise ValueError("XP level must be a positive integer.")
        
        if self.pfp and not isinstance(self.pfp, str):
            raise ValueError("Profile picture must be a string (e.g., URL or filename).")
        
        if self.pfp and not self.pfp.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise ValueError("Profile picture must be a valid image file.")
        