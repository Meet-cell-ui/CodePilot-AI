from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.api_key_manager import validate_api_key


API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(
    name=API_KEY_NAME,
    auto_error=False
)


def verify_api_key(api_key: str = Depends(api_key_header)):
    """
    Verify the CodePilot API key supplied
    through the X-API-Key header.
    """

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required."
        )

    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or inactive API key."
        )

    return api_key
