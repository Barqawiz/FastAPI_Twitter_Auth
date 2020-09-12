from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

tw_request_invalid = HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                   detail="Failed to get twitter request token.")

tw_access_invalid = HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                  detail="Failed to get twitter access token.")