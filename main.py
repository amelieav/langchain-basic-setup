from dotenv import load_dotenv
import os

"""Load in secrets from .env file, if cloning this repo then ensure you add your own .env file"""

load_dotenv()
api_key = os.getenv('API_KEY')


