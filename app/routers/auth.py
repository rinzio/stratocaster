from typing import Annotated
from http import HTTPStatus as HTTP

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from typing import Any, List, Dict


from internal.db.models.user import BaseUserModel
from internal.env import AUTH_EXPIRE

from ..auth import AuthManager
from ..dependencies import current_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={HTTP.NOT_FOUND: {"description": "Not found"}},
)

@router.post("/login")
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Dict[str, str]:
    user = AuthManager.login(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AuthManager.create_token(
        data={"username": user.email}, expires_in=AUTH_EXPIRE
    )
    return dict(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=BaseUserModel)
async def me(
    sui: Annotated[BaseUserModel, Depends(current_user)],
):
    return sui

