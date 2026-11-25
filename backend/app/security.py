import hmac
from fastapi import Header, HTTPException, status
from app.config import settings

def verify_beta_access(
    x_beta_code: str | None = Header(default=None)
):
    expected_code = settings.BETA_ACCESS_CODE

    if (
        not expected_code
        or not x_beta_code
        or not hmac.compare_digest(x_beta_code, expected_code)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing beta access code."
        )
