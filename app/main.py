import os
import time
import logging
import hashlib
import redis
import google.generativeai as genai
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Advanced Logging Setup (Daily Rotation)
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

logger = logging.getLogger("gemini-bridge")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=30)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

# 3. App & Connections
app = FastAPI(title="FastAPI Gemini Bridge")

try:
    # Initialize Redis with password from Dify's config
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD"), # This will now be 'difyai123456'
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True
    )
    r.ping()
    logger.info("Connected to Redis successfully.")
except Exception as e:
    logger.critical(f"Redis connection failed: {e}")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 4. Helper: Calculate File Hash
def calculate_hash(file_content: bytes):
    """Calculate SHA256 to uniquely identify files across different projects."""
    return hashlib.sha256(file_content).hexdigest()

@app.post("/v1/files/upload")
async def upload_file_to_gemini(
    file: UploadFile = File(...),
    project_id: str = Form("default") # Identify which project is calling
):
    """
    Receives file from Dify/Other projects, caches by hash, and uploads to Gemini.
    """
    logger.info(f"RECEIVED REQUEST: Project='{project_id}', Filename='{file.filename}'")
    
    try:
        # Read file content
        content = await file.read()
        file_hash = calculate_hash(content)
        cache_key = f"gemini_file:{file_hash}"

        # Step 1: Check Global Cache
        cached_uri = r.get(cache_key)
        if cached_uri:
            logger.info(f"CACHE HIT: File hash {file_hash} already exists. Returning URI.")
            return {"hit": True, "gemini_uri": cached_uri, "hash": file_hash}

        # Step 2: Cache Miss - Save temporary for Gemini SDK
        temp_path = f"temp_{file_hash}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)

        # Step 3: Upload to Gemini File API
        logger.info(f"CACHE MISS: Uploading new file to Gemini...")
        start_time = time.time()
        gemini_file = genai.upload_file(path=temp_path, display_name=file.filename)
        
        # Cleanup temp file
        os.remove(temp_path)

        # Step 4: Update Redis (47 Hours TTL)
        r.setex(cache_key, 169200, gemini_file.uri)
        
        duration = time.time() - start_time
        logger.info(f"UPLOAD SUCCESS: URI={gemini_file.uri} in {duration:.2f}s")

        return {
            "hit": False, 
            "gemini_uri": gemini_file.uri, 
            "hash": file_hash,
            "project": project_id
        }

    except Exception as e:
        logger.error(f"PROCESS ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 60060))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)