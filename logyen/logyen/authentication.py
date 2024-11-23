from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .config import KeycloakConfig
from .mongoData import findUser


class KeycloakMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(prefix) for prefix in ("/static", "/auth")):
            return await call_next(request)
        if request.url.path in KeycloakConfig.UNPROTECTED_ENDPOINTS:
            return await call_next(request)

        access_token = request.cookies.get("access_token")
        if access_token:
            try:
                user_info = KeycloakConfig.keycloak_openid.userinfo(access_token)
                user_info["token"] = access_token
                request.state.user = user_info
                user = findUser(user_info["email"])
                request.state.userMetadata = user
                return await call_next(request)

            except Exception as e:
                return JSONResponse({"code": 8000, "message": "Invalid token."})
        else:
            return JSONResponse({"code": 8001, "message": "Authorization header missing."})


def extractUserFromToken(token: str):
    try:
        user_info = KeycloakConfig.keycloak_openid.userinfo(token)
        user = findUser(user_info["email"])
        return user
    except Exception:
        return None
