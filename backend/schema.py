from database import Database
from config import (
    CARDS_COLLECTION, CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, 
    PROFILES_COLLECTION, CLASH_ROYALE_API_KEY, CLASH_ROYALE_API_URL
)
import requests
import json

def fetch_clash_royale_cards():
    """Fetch card data from Clash Royale API"""
    if not CLASH_ROYALE_API_KEY:
        raise ValueError("Clash Royale API key not found. Please set CLASH_ROYALE_API_KEY in your .env file")

    headers = {
        'Authorization': f'Bearer {CLASH_ROYALE_API_KEY}',
        'Accept': 'application/json'
    }

    try:
        print(f"Fetching cards from Clash Royale API...")
        response = requests.get(f'{CLASH_ROYALE_API_URL}/cards', headers=headers)
        print(f"API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"API Error Response: {response.text}")
        response.raise_for_status()
        cards = response.json().get('items', [])
        print(f"Successfully fetched {len(cards)} cards from API")
        return cards
    except requests.RequestException as e:
        print(f"Error fetching Clash Royale cards: {str(e)}")
        return []

def transform_clash_royale_card(card):
    """Transform Clash Royale card data to match our schema"""
    # Map Clash Royale rarities to our rarity system
    rarity_mapping = {
        'Common': 'common',
        'Rare': 'rare',
        'Epic': 'epic',
        'Legendary': 'legendary',
        'Champion': 'champion'
    }

    # Get the rarity from the maxLevel
    rarity = None
    max_level = card.get('maxLevel', 14)
    if max_level == 14:
        rarity = 'Common'
    elif max_level == 12:
        rarity = 'Rare'
    elif max_level == 9:
        rarity = 'Epic'
    elif max_level == 6:
        rarity = 'Legendary'
    elif max_level == 4:
        rarity = 'Champion'
    
    return {
        "_id": str(card.get('id', '')),
        "name": card.get('name', ''),
        "rarity": rarity_mapping.get(rarity, 'common'),  # Default to common if unknown
        "icon": card.get('iconUrls', {}).get('medium', 'default.png'),
        "cost": card.get('elixirCost', 1)
    }

def setup_database():
    # Get database instance
    db = Database().db
    print("Connected to MongoDB database")

    # Create collections if they don't exist
    if CARDS_COLLECTION not in db.list_collection_names():
        print("Cards collection not found, creating it...")
        db.create_collection(CARDS_COLLECTION)
        
        # Fetch and transform Clash Royale cards
        clash_cards = fetch_clash_royale_cards()
        if clash_cards:
            transformed_cards = [transform_clash_royale_card(card) for card in clash_cards]
            print(f"Inserting {len(transformed_cards)} cards into database...")
            db[CARDS_COLLECTION].insert_many(transformed_cards)
            print("Cards successfully inserted into database")
        else:
            print("Warning: No cards fetched from Clash Royale API")

    # Create other collections if they don't exist
    for collection in [CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, PROFILES_COLLECTION]:
        if collection not in db.list_collection_names():
            db.create_collection(collection)

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
                    "rarity": {"enum": ["common", "rare", "epic", "legendary", "champion"]},
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
                "required": ["_id", "profile_id", "card_id", "unlocked", "level", "copiesOwned"],
                "properties": {
                    "_id": {"bsonType": "string"},
                    "profile_id": {"bsonType": "string"},
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
                "required": ["username", "xp_lvl"],
                "properties": {
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