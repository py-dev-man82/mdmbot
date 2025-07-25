import requests
import hashlib
from config import MDM_API_URL, MDM_USER, MDM_PASS, logger

jwt_token = None

def md5_upper(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest().upper()

def api_login():
    global jwt_token
    logger.debug("MDM API login...")
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

def get_device_info(device_id_or_name):
    logger.debug(f"Searching for device: {device_id_or_name}")
    url = f"{MDM_API_URL}/private/devices/search"
    payload = {"pageSize": 1000, "pageNum": 1}
    resp = requests.post(url, json=payload, headers=api_headers())
    if resp.status_code == 401:
        logger.warning("JWT expired, re-authenticating...")
        api_login()
        resp = requests.post(url, json=payload, headers=api_headers())
    resp.raise_for_status()
    devices = resp.json().get("devices", [])
    for d in devices:
        if str(d.get("id")) == str(device_id_or_name) or d.get("deviceName") == device_id_or_name:
            logger.info(f"Device found: {d}")
            return d
    logger.info("Device not found.")
    return None

def add_device(device_info):
    logger.debug(f"Adding device: {device_info}")
    # Try using PUT /private/devices for newest API; fallback to POST if needed
    url = f"{MDM_API_URL}/private/devices"
    resp = requests.put(url, json=device_info, headers=api_headers())
    if resp.status_code in (404, 405):
        url = f"{MDM_API_URL}/private/device/create"
        resp = requests.post(url, json=device_info, headers=api_headers())
    if resp.status_code == 401:
        logger.warning("JWT expired, re-authenticating...")
        api_login()
        resp = requests.put(url, json=device_info, headers=api_headers())
    resp.raise_for_status()
    logger.info("Device added successfully.")
    return resp.json()

def wipe_device(device_id):
    logger.debug(f"Wiping device: {device_id}")
    url = f"{MDM_API_URL}/plugins/devicereset/private/reset/{device_id}"
    resp = requests.put(url, headers=api_headers())
    if resp.status_code == 401:
        logger.warning("JWT expired, re-authenticating...")
        api_login()
        resp = requests.put(url, headers=api_headers())
    resp.raise_for_status()
    logger.info("Wipe command sent.")
    return resp.json() if resp.text else {}

def delete_device(device_id):
    logger.debug(f"Deleting device: {device_id}")
    url = f"{MDM_API_URL}/private/devices/{device_id}"
    resp = requests.delete(url, headers=api_headers())
    if resp.status_code == 401:
        logger.warning("JWT expired, re-authenticating...")
        api_login()
        resp = requests.delete(url, headers=api_headers())
    resp.raise_for_status()
    logger.info("Device deleted successfully.")
    return resp.json() if resp.text else {}
