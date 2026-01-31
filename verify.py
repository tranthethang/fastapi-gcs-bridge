# verify.py - Comprehensive verification for fastapi-gcs-bridge
# Full comments and logging in English as requested

import requests
import os
import hashlib
from dotenv import load_dotenv

# 1. Load configuration
load_dotenv()
APP_PORT = os.getenv("APP_PORT", "60060")
BASE_URL = f"http://127.0.0.1:{APP_PORT}"
UPLOAD_URL = f"{BASE_URL}/v1/files/upload"

def calculate_file_hash(path):
    """Generate SHA256 hash of the file to verify against API response."""
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def run_verification():
    print("=== FASTAPI GCS BRIDGE VERIFICATION ===")
    
    # Test 1: Check if Server is alive
    print(f"[*] Testing connection to {BASE_URL}...")
    try:
        # FastAPI docs is a good health check endpoint
        requests.get(f"{BASE_URL}/docs", timeout=5)
        print("[+] Server is UP and reachable.")
    except Exception as e:
        print(f"[-] CRITICAL: Server is DOWN or unreachable at {BASE_URL}")
        return

    # Test 2: Perform Real Upload
    test_file = "assets/global_v1.pdf"
    if not os.path.exists(test_file):
        # Create a dummy file if assets doesn't exist for testing
        os.makedirs("assets", exist_ok=True)
        with open(test_file, "w") as f:
            f.write("Dummy PDF content for verification.")
        print(f"[!] Created dummy file for testing: {test_file}")

    local_hash = calculate_file_hash(test_file)
    print(f"[*] Local File Hash: {local_hash}")

    files = {
        'file': (os.path.basename(test_file), open(test_file, 'rb'), 'application/pdf')
    }
    data = {'project_id': 'VERIFICATION_TEST'}

    print(f"[*] Sending Upload Request (First attempt)...")
    try:
        response = requests.post(UPLOAD_URL, files=files, data=data)
        response.raise_for_status()
        res_data = response.json()
        
        print(f"[+] Response Status: {response.status_code}")
        print(f"    Gemini URI: {res_data.get('gemini_uri')}")
        
        # Test 3: Verify Cache (Second attempt)
        print(f"[*] Sending Upload Request (Second attempt - Cache Test)...")
        # Re-open file for second stream
        files['file'] = (os.path.basename(test_file), open(test_file, 'rb'), 'application/pdf')
        response_v2 = requests.post(UPLOAD_URL, files=files, data=data)
        res_v2 = response_v2.json()
        
        if res_v2.get('hit') is True:
            print("[+] CACHE SUCCESS: Hash-based deduplication is working.")
        else:
            print("[-] CACHE FAILURE: Server did not return hit:True for the same file.")

        # Final Hash Validation
        if res_v2.get('hash') == local_hash:
            print("[+] HASH MATCH: Server-side SHA256 matches local SHA256.")
        else:
            print("[-] HASH MISMATCH: Verification failed.")

    except Exception as e:
        print(f"[-] TEST FAILED: {str(e)}")

if __name__ == "__main__":
    run_verification()