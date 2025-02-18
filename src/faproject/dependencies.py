from datetime import datetime

from django.contrib.auth.models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"  # Move to environment variables
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user from JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401)
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401)

#     user = User.objects.filter(username=username).first()
#     if user is None:
#         raise HTTPException(status_code=401)
#     return user
