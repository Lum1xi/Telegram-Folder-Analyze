from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
OWNER_ID = int(os.getenv("OWNER_ID"))
DB_PATH = os.getenv("DB_PATH", "users.db")
GEMINI_KEY = os.getenv("GEMINI_KEY")