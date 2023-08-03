from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import create_token, valid_token

# define class JWTBearer
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # get user credential
        auth = await super().__call__(request)
        # valid token with user credential
        data: dict = valid_token(auth.credentials)
        # valid credentials
        if data['email'] != "admin@admin.com":
            # generate HTTP exception
            raise HTTPException(status_code = 403, detail = "Invalid credentials")