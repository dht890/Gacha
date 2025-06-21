import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DATABASE_NAME = 'game'

# Collection Names
CARDS_COLLECTION = 'cards'
CHESTS_COLLECTION = 'chests'
USER_COLLECTIONS_COLLECTION = 'user_collections'
PROFILES_COLLECTION = 'profiles'

# Clash Royale API Configuration
CLASH_ROYALE_API_KEY = os.getenv('CLASH_ROYALE_API_KEY')
CLASH_ROYALE_API_URL = 'https://api.clashroyale.com/v1'

