from database import Database
from models import Profile, UserCollection, Card, Chest
from config import CARDS_COLLECTION, CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, PROFILES_COLLECTION
from schema import setup_database

# Initialize database schema
setup_database()

# Get database instance
db = Database().db

# Get collections
cards = db.get_collection(CARDS_COLLECTION)
profiles = db.get_collection(PROFILES_COLLECTION)
chests = db.get_collection(CHESTS_COLLECTION)
user_collections = db.get_collection(USER_COLLECTIONS_COLLECTION)

# Your application routes and logic will go here...
