import requests
from config import MDM_API_URL, logger

def get_device_info(device_id):
    """
    Looks up device by ID, IMEI, or name.
    Returns device dict or None if not found.
    """
    token = get_jwt_token()  # Or however you store/access it
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "pageNum": 1,
        "pageSize": 1,
        "searchValue": device_id,
        "sortField": "id",
        "sortOrder": "asc"
    }
    url = f"{MDM_API_URL}/private/devices/search"
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()
    devices = data.get("items", [])
    return devices[0] if devices else None
