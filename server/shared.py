from fastapi import HTTPException


def create_http_exception(status_code: int, reason: str, **kwargs):
    return HTTPException(
        status_code, {"status_code": status_code, "reason": reason, **kwargs}
    )
