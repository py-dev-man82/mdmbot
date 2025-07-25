import requests
import hashlib
import os
import time
from config import MDM_API_URL, MDM_USER, MDM_PASS, logger

TOKEN_FILE = "mdm_token.txt"
TOKEN_EXPIRY_FILE = "mdm_token_expiry.txt"

def _save_token(token, expires_in=82800):  # 82800s ≈ 23h
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    # Save expiry timestamp (for auto refresh)
    expires_at = int(time.time()) + expires_in - 300  # 5 min early
    with open(TOKEN_EXPIRY_FILE, "w") as f:
        f.write(str(expires_at))

def _load_token():
    if not os.path.isfile(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        token = f.read().strip()
    # Check expiry
    if os.path.isfile(TOKEN_EXPIRY_FILE):
        with open(TOKEN_EXPIRY_FILE) as f:
            expires_at = int(f.read().strip())
        if time.time() >= expires_at:
            return None
    return token

def get_jwt_token():
    # Try to load token from file and check if still valid
    token = _load_token()
    if token:
        return token
    # If not, log in and get a new one
    logger.info("Fetching new JWT token from MDM API...")
    url = f"{MDM_API_URL}/public/jwt/login"
    password_md5 = hashlib.md5(MDM_PASS.encode('utf-8')).hexdigest().upper()
    payload = {"login": MDM_USER, "password": password_md5}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    data = r.json()
    token = data.get("id_token")
    if not token:
        logger.error("No JWT token in login response!")
        raise RuntimeError("Failed to obtain JWT token!")
    _save_token(token)
    return token

def get_device_info(device_id):
    """
    Looks up device by ID, IMEI, or name.
    Returns device dict or None if not found.
    """
    token = get_jwt_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "pageNum": 1,
        "pageSize": 1,
        "searchValue": device_id,
        "sortField": "id",
        "sortOrder": "asc"
    }
    url = f"{MDM_API_URL}/private/devices/search"
    logger.debug(f"Querying device info from: {url} with payload {payload}")
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    if r.status_code == 401:
        # Token expired or invalid; try to get a new one once
        logger.warning("JWT token expired, refreshing…")
        os.remove(TOKEN_FILE)
        os.remove(TOKEN_EXPIRY_FILE)
        token = get_jwt_token()
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(url, headers=headers, json=payload, timeout=10)
    r.raise_for_status()
    data = r.json()
    devices = data.get("items", [])
    logger.debug(f"Device search result: {devices}")
    return devices[0] if devices else None

# (Add more API helper functions below as needed...)
