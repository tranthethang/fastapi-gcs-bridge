import os

import google.generativeai as genai

from app.config import Config
from app.logger import logger


class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)

    def upload_file(self, temp_path: str, filename: str):
        try:
            logger.info("CACHE MISS: Uploading new file to Gemini...")
            gemini_file = genai.upload_file(path=temp_path, display_name=filename)
            return gemini_file
        except Exception as e:
            logger.error(f"GEMINI UPLOAD ERROR: {str(e)}")
            raise e
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


gemini_service = GeminiService()
