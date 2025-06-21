from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from models import Profile, UserCollection, Card, Chest
from config import CARDS_COLLECTION, CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, PROFILES_COLLECTION
from schema import setup_database, fetch_clash_royale_cards, transform_clash_royale_card
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database schema
setup_database()

# Get database instance
db = Database().db

# Get collections
cards = db.get_collection(CARDS_COLLECTION)
profiles = db.get_collection(PROFILES_COLLECTION)
chests = db.get_collection(CHESTS_COLLECTION)
user_collections = db.get_collection(USER_COLLECTIONS_COLLECTION)

def get_or_create_profile():
    """Get the local profile or create it if it doesn't exist"""
    profile = profiles.find_one({})  # Get any profile since we'll only have one
    
    if not profile:
        print("Creating local profile...")
        # Get all cards from the database
        all_cards = list(cards.find())
        
        if not all_cards:
            raise ValueError("No cards found in the database. Please ensure the database is properly initialized.")
        
        # Create a new profile
        new_profile = {
            "username": "LocalPlayer",
            "xp_lvl": 1,
            "pfp": "default.png"
        }
        
        # Insert the profile into the database
        profile_result = profiles.insert_one(new_profile)
        
        # Create user collection entries for each card
        user_card_collection = []
        for card in all_cards:
            collection_entry = {
                "_id": str(ObjectId()),  # Generate a new unique ID for each card in the collection
                "profile_id": str(profile_result.inserted_id),  # Link to the profile
                "card_id": str(card["_id"]),
                "unlocked": False,
                "level": 1,
                "copiesOwned": 0
            }
            user_card_collection.append(collection_entry)
        
        # Insert the collection into the database
        user_collections.insert_many(user_card_collection)
        print("Local profile created successfully")
        
        profile = profiles.find_one({"_id": profile_result.inserted_id})
    
    return profile

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Clash Royale Card Game API"}), 200

@app.route('/api/profile', methods=['GET'])
def get_profile():
    try:
        profile = get_or_create_profile()
        
        # Convert ObjectId to string for JSON serialization
        profile_id = str(profile['_id'])
        profile['_id'] = profile_id
        
        # Get user's card collection
        user_card_collection = list(user_collections.find({"profile_id": profile_id}))
        
        # Convert ObjectIds and add card details
        for card in user_card_collection:
            if '_id' in card:
                card['_id'] = str(card['_id'])
            if 'profile_id' in card:
                card['profile_id'] = str(card['profile_id'])
            if 'card_id' in card:
                card['card_id'] = str(card['card_id'])
                
                # Get card details
                card_details = cards.find_one({"_id": card["card_id"]})
                if card_details:
                    card["name"] = card_details.get("name")
                    card["rarity"] = card_details.get("rarity")
                    card["icon"] = card_details.get("icon")
                    card["cost"] = card_details.get("cost")
        
        # Add collection to profile response
        profile['collection'] = user_card_collection
        
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/cards/refresh', methods=['POST'])
def refresh_cards():
    try:
        # Clear existing cards
        cards.delete_many({})
        
        # Fetch new cards
        clash_cards = fetch_clash_royale_cards()
        if clash_cards:
            transformed_cards = [transform_clash_royale_card(card) for card in clash_cards]
            cards.insert_many(transformed_cards)
            return jsonify({"message": f"Successfully refreshed {len(transformed_cards)} cards"}), 200
        else:
            return jsonify({"error": "No cards fetched from Clash Royale API"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/cards', methods=['GET'])
def get_cards():
    try:
        all_cards = list(cards.find({}, {'_id': 1, 'name': 1, 'rarity': 1, 'icon': 1, 'cost': 1}))
        # Convert ObjectId to string for JSON serialization
        for card in all_cards:
            card['_id'] = str(card['_id'])
        return jsonify(all_cards), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Initialize database schema
    setup_database()
    # Ensure we have a local profile
    get_or_create_profile()
    app.run(debug=True, port=5000)