import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    APP_PORT = int(os.getenv("APP_PORT", 60060))
    CACHE_TTL = 169200  # 47 hours
