import requests
import hashlib
from config import MDM_API_URL, MDM_USER, MDM_PASS, logger

jwt_token = None

def md5_upper(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest().upper()

def api_login():
    global jwt_token
    logger.debug("Attempting MDM API login...")
    resp = requests.post(
        f"{MDM_API_URL}/public/jwt/login",
        json={"login": MDM_USER, "password": md5_upper(MDM_PASS)}
    )
    resp.raise_for_status()
    jwt_token = resp.json()["id_token"]
    logger.info("Obtained JWT token.")
    return jwt_token

def api_headers():
    if not jwt_token:
        api_login()
    return {"Authorization": f"Bearer {jwt_token}"}

def logout():
    global jwt_token
    jwt_token = None
    logger.info("Logged out, JWT cleared.")
