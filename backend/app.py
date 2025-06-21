from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from models import Profile, UserCollection, Card, Chest
from config import CARDS_COLLECTION, CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, PROFILES_COLLECTION
from schema import setup_database, fetch_clash_royale_cards, transform_clash_royale_card

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

@app.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    try:
        profile = profiles.find_one({"username": username})
        if profile:
            # Convert ObjectId to string for JSON serialization
            profile['_id'] = str(profile['_id'])
            
            # Convert ObjectIds in the collection
            for card in profile.get('collection', []):
                if '_id' in card:
                    card['_id'] = str(card['_id'])
                if 'card_id' in card:
                    card['card_id'] = str(card['card_id'])
            
            return jsonify(profile), 200
        else:
            return jsonify({"error": "Profile not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/profile', methods=['POST'])
def create_profile():
    data = request.json
    username = data.get('username')
    pfp = data.get('pfp', 'default.png')
    
    try:
        create_new_profile(username, pfp)
        return jsonify({"message": "Profile created successfully"}), 201
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

def create_new_profile(username, pfp="default.png"):
    """Create a new user profile with an empty card collection"""
    # Get all cards from the database
    all_cards = list(cards.find())
    
    if not all_cards:
        raise ValueError("No cards found in the database. Please ensure the database is properly initialized.")
    
    # Create user collection entries for each card
    user_card_collection = []
    for card in all_cards:
        collection_entry = {
            "card_id": str(card["_id"]),
            "unlocked": False,
            "level": 1,
            "copiesOwned": 0
        }
        user_card_collection.append(collection_entry)
    
    # Insert the collection into the database
    collection_result = user_collections.insert_many(user_card_collection)
    
    # Create a new profile with the collection
    new_profile = {
        "id": "1",  # You might want to generate this dynamically
        "username": username,
        "xp_lvl": 1,
        "pfp": pfp,
        "collection": user_card_collection
    }
    
    # Insert the profile into the database
    profiles.insert_one(new_profile)
    print("Profile created successfully")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

