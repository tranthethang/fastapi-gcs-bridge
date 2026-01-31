# FastAPI Gemini Bridge

A centralized file service designed to act as an intermediary between client applications and the **Gemini File API**. It optimizes file handling by providing hash-based deduplication and caching, preventing redundant uploads to Google's infrastructure.

## 🚀 Features

- **Efficient File Uploads**: Receives files via multipart/form-data and proxies them to the Gemini File API.
- **Hash-based Deduplication**: Calculates SHA256 hashes of file contents to identify identical files.
- **Redis Caching**: Stores Gemini URIs in Redis with a 47-hour TTL (169,200 seconds) to ensure quick retrieval of previously uploaded files.
- **Project Isolation**: Supports optional `project_id` for better organization and tracking of uploads.
- **Daily Rotating Logs**: Built-in logging with rotation to keep track of operations and troubleshoot issues.
- **Verification Suite**: Includes a `verify.py` script to validate server health, upload functionality, and cache integrity.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Cache**: [Redis](https://redis.io/)
- **SDK**: [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- **Environment Management**: [python-dotenv](https://github.com/theskumar/python-dotenv)

## 📋 Prerequisites

- Python 3.9+
- Redis Server (running and accessible)
- Google Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/))

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fastapi-gcs-bridge
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Copy the example environment file and update it with your credentials:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in:
   - `GEMINI_API_KEY`: Your Google AI Studio API key.
   - `REDIS_HOST`: Hostname of your Redis server.
   - `REDIS_PORT`: Port of your Redis server (default: 6379).
   - `REDIS_PASSWORD`: Password for your Redis server.

## 🏃 Running the Application

### Start the Server
Run the application using the built-in launcher:
```bash
python app/main.py
```
The server will start on `0.0.0.0` at the port specified in your `.env` (default `60060`).

### Verify Installation
You can run the verification script to ensure everything is configured correctly:
```bash
python verify.py
```

## 🔌 API Usage

### Upload a File
**Endpoint**: `POST /v1/files/upload`

**Request Parameters**:
- `file` (File, required): The file to be uploaded.
- `project_id` (Form Data, optional): A string identifier for the project.

**Example using cURL**:
```bash
curl -X POST http://localhost:60060/v1/files/upload \
  -F "file=@/path/to/your/document.pdf" \
  -F "project_id=my_project_alpha"
```

**Response**:
```json
{
  "hit": false,
  "gemini_uri": "https://generativelanguage.googleapis.com/v1beta/files/...",
  "hash": "sha256_hash_of_the_file",
  "project": "my_project_alpha"
}
```
*Note: `hit: true` indicates the file was served from cache and not re-uploaded to Gemini.*

## 📁 Project Structure

- `app/`: Core application directory.
  - `api/`: API route definitions.
  - `services/`: Business logic for Gemini and Redis interactions.
  - `utils/`: Helper functions (e.g., hash calculation).
  - `main.py`: Application entry point.
- `logs/`: Directory for log files.
- `verify.py`: Testing and validation script.
- `requirements.txt`: Python dependencies.
