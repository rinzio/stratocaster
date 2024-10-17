from typing import Annotated
from http import HTTPStatus as HTTP

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException


from internal.env import AUTH_SECRET_KEY, AUTH_ALGORITHM
from internal.db.models.user import BaseUserModel, Role
from internal.db.repository import UserRepo


async def current_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))]):
    auth_err = HTTPException(
        status_code=HTTP.UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        email: str | None = payload.get("username")
        user = UserRepo.get(email=email)
        if user is None:
            raise auth_err
    except InvalidTokenError:
        raise auth_err

    if user is not None and user.is_active:   
        return user
    raise auth_err


async def is_admin(user: Annotated[BaseUserModel, Depends(current_user)]):
    auth_err = HTTPException(
        status_code=HTTP.FORBIDDEN,
        detail="Not authorized to use this resource",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if Role(user.role) != Role.ADMIN:
        raise auth_err
    return user


async def is_doctor(user: Annotated[BaseUserModel, Depends(current_user)]):
    auth_err = HTTPException(
        status_code=HTTP.FORBIDDEN,
        detail="Not authorized to use this resource",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if Role(user.role) != Role.DOCTOR:
        raise auth_err
    return user