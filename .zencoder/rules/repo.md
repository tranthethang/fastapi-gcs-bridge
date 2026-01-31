---
description: Repository Information Overview
alwaysApply: true
---

# FastAPI Gemini Bridge Information

## Summary
The **FastAPI Gemini Bridge** is a centralized file service designed to act as an intermediary between client applications (like Dify) and the **Gemini File API**. It provides features such as file upload reception, hash-based caching using **Redis** to prevent redundant uploads, and daily rotating logs.

## Structure
- [./app/](./app/): Contains the core application logic.
    - [./app/main.py](./app/main%2Epy): The main **FastAPI** entry point.
- [./logs/](./logs/): Directory where daily rotating log files are stored.
- [./requirements.txt](./requirements%2Etxt): List of Python dependencies.
- [./verify.py](./verify%2Epy): A client simulation script used for testing the file upload process.
- [./.env.example](./%2Eenv%2Eexample): Template for environment variables including **Redis** and **Gemini API** configurations.

## Language & Runtime
**Language**: Python  
**Version**: 3.x (FastAPI compatible)  
**Build System**: pip  
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- **fastapi**: Web framework for building APIs.
- **uvicorn**: ASGI server for running the FastAPI application.
- **redis**: Client for the Redis cache.
- **google-generativeai**: SDK for interacting with Google's Gemini models and File API.
- **python-dotenv**: For loading environment variables from a `.env` file.
- **google-cloud-storage**: For GCS integration (though primarily Gemini File API is used in `main.py`).

## Build & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your GEMINI_API_KEY and REDIS details
```

## Main Files & Resources
- **App Entry Point**: [./app/main.py](./app/main%2Epy)
- **Configuration**: [./.env](./%2Eenv) (created from [./.env.example](./%2Eenv%2Eexample))
- **Logs**: Managed via `TimedRotatingFileHandler` in [./app/main.py](./app/main%2Epy:26), rotating at midnight.

## Testing & Validation
**Validation Script**: [./verify.py](./verify%2Epy)
**Functionality**: Simulates a multipart form-data upload to the `/v1/files/upload` endpoint.
**Requirements**: Requires a test file (e.g., `assets/global_v1.pdf`) and the server to be running.

**Run Server**:
```bash
# From the project root
python app/main.py
```

**Run Validation**:
```bash
python verify.py
```
