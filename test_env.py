import os

from dotenv import load_dotenv

load_dotenv()

print("PYTHONPATH from .env:", os.getenv("PYTHONPATH"))
