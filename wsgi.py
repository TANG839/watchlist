import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)        # Load environment variables from .env file

from watchlist import app           # Import the app object from the watchlist package