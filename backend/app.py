from database import Database
from models import Profile, UserCollection, Card, Chest
from config import CARDS_COLLECTION, CHESTS_COLLECTION, USER_COLLECTIONS_COLLECTION, PROFILES_COLLECTION
from pymongo.errors import DuplicateKeyError

#how to access the database
db = Database().client.game

#how to access a collection
cards = db.cards
profiles = db.profiles
chests = db.chests
user_collections = db.user_collections
