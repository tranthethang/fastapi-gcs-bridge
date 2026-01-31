import redis

from app.config import Config
from app.logger import logger


class RedisService:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                password=Config.REDIS_PASSWORD,
                db=Config.REDIS_DB,
                decode_responses=True,
            )
            self.client.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.critical(f"Redis connection failed: {e}")
            raise e

    def get_uri(self, file_hash: str) -> str:
        cache_key = f"gemini_file:{file_hash}"
        return self.client.get(cache_key)

    def set_uri(self, file_hash: str, uri: str):
        cache_key = f"gemini_file:{file_hash}"
        self.client.setex(cache_key, Config.CACHE_TTL, uri)


redis_service = RedisService()
