---
description: Repository Information Overview
alwaysApply: true
---

# FastAPI Gemini Bridge Information

## Summary
The **FastAPI Gemini Bridge** is a centralized file service designed to act as an intermediary between client applications (like Dify) and the **Gemini File API**. It features file upload reception, hash-based caching using **Redis** to prevent redundant uploads (with a 47-hour TTL), and daily rotating logs.

## Structure
- [./app/](./app/): Core application logic.
    - [./app/main.py](./app/main%2Epy): Main **FastAPI** entry point with Redis and Gemini configuration.
- [./logs/](./logs/): Directory for daily rotating log files (`TimedRotatingFileHandler`).
- [./requirements.txt](./requirements%2Etxt): Project dependencies.
- [./verify.py](./verify%2Epy): Comprehensive verification script to test server connectivity, file uploads, and hash-based deduplication.
- [./.env.example](./%2Eenv%2Eexample): Configuration template for environment variables.

## Language & Runtime
**Language**: Python  
**Version**: 3.x  
**Build System**: pip  
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- **fastapi**: Web framework for building APIs.
- **uvicorn**: ASGI server.
- **redis**: Client for the Redis cache (supports password authentication).
- **google-generativeai**: SDK for Google's Gemini models and File API.
- **python-dotenv**: For environment variable management.
- **python-multipart**: Required for handling file uploads in FastAPI.
- **google-cloud-storage**: Integrated for GCS functionality.

## Build & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Required: GEMINI_API_KEY, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
```

## Main Files & Resources
- **App Entry Point**: [./app/main.py](./app/main%2Epy) (Runs on `APP_PORT`, default `60060`).
- **Configuration**: Managed via `.env` file using [./.env.example](./%2Eenv%2Eexample).
- **Caching**: Uses **Redis** with SHA256 file hashes as keys (`gemini_file:{hash}`).

## Testing & Validation
**Validation Script**: [./verify.py](./verify%2Epy)  
**Tests Performed**:
1. Server connectivity check (`/docs` endpoint).
2. Multipart file upload to `/v1/files/upload`.
3. Cache hit verification (deduplication test).
4. Hash integrity validation (SHA256).

**Run Commands**:
```bash
# Start the server
python app/main.py

# Execute verification suite
python verify.py
```
