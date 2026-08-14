import secrets
import hashlib
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY_FILE = os.path.join(BASE_DIR, "api_keys.json")


def _hash_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def _load_keys():
    if not os.path.exists(API_KEY_FILE):
        return {}

    try:
        with open(API_KEY_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_keys(keys):
    with open(API_KEY_FILE, "w") as file:
        json.dump(keys, file, indent=4)


def create_api_key():
    """
    Generate a new CodePilot API key.
    The raw key is returned only once.
    """

    api_key = "cpai_" + secrets.token_urlsafe(32)

    key_hash = _hash_key(api_key)

    keys = _load_keys()

    keys[key_hash] = {
        "name": "CodePilot Client",
        "active": True
    }

    _save_keys(keys)

    return api_key


def validate_api_key(api_key: str) -> bool:
    """
    Validate a CodePilot API key.
    """

    if not api_key:
        return False

    key_hash = _hash_key(api_key)

    keys = _load_keys()

    key_data = keys.get(key_hash)

    if not key_data:
        return False

    return key_data.get("active", False)
