from database import Database
from config import CARDS_COLLECTION, CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, PROFILES_COLLECTION

def setup_database():
    # Get database instance
    db = Database().db

    # Create collections if they don't exist
    if CARDS_COLLECTION not in db.list_collection_names():
        db.create_collection(CARDS_COLLECTION)

    if CHESTS_COLLECTION not in db.list_collection_names():
        db.create_collection(CHESTS_COLLECTION)

    if USER_COLLECTIONS_COLLECTION not in db.list_collection_names():
        db.create_collection(USER_COLLECTIONS_COLLECTION)

    if PROFILES_COLLECTION not in db.list_collection_names():
        db.create_collection(PROFILES_COLLECTION)

    # Apply validators
    apply_card_collection_validator(db)
    apply_chest_collection_validator(db)
    apply_user_collection_validator(db)
    apply_profile_collection_validator(db)

def apply_card_collection_validator(db):
    db.command({
        "collMod": CARDS_COLLECTION,
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "rarity", "icon", "cost"],
                "properties": {
                    "name": {"bsonType": "string"},
                    "rarity": {"enum": ["common", "rare", "epic", "legendary"]},
                    "icon": {"bsonType": "string"},
                    "cost": {
                        "bsonType": "int",
                        "minimum": 1,
                        "maximum": 10
                    }
                }
            }
        },
        "validationLevel": "strict"
    })

def apply_chest_collection_validator(db):
    db.command({
        "collMod": CHESTS_COLLECTION,
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["type", "dropRate", "contents"],
                "properties": {
                    "type": {"bsonType": "string"},
                    "dropRate": {
                        "bsonType": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "contents": {
                        "bsonType": "object",
                        "required": ["cards"],
                        "properties": {
                            "cards": {
                                "bsonType": "object",
                                "required": ["distribution"],
                                "properties": {
                                    "distribution": {"bsonType": "object"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "validationLevel": "strict"
    })

def apply_user_collection_validator(db):
    db.command({
        "collMod": USER_COLLECTIONS_COLLECTION,
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["card_id", "unlocked", "level", "copiesOwned"],
                "properties": {
                    "card_id": {"bsonType": "string"},
                    "unlocked": {"bsonType": "bool"},
                    "level": {
                        "bsonType": "int",
                        "minimum": 0
                    },
                    "copiesOwned": {
                        "bsonType": "int",
                        "minimum": 0
                    }
                }
            }
        },
        "validationLevel": "strict"
    })

def apply_profile_collection_validator(db):
    db.command({
        "collMod": PROFILES_COLLECTION,
        "validator": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["id", "username", "xp_lvl"],
                "properties": {
                    "id": {"bsonType": "string"},
                    "username": {"bsonType": "string"},
                    "xp_lvl": {
                        "bsonType": "int",
                        "minimum": 1
                    },
                    "pfp": {
                        "bsonType": ["string", "null"]
                    }
                }
            }
        },
        "validationLevel": "strict"
    }) 