from http import HTTPStatus as status

from fastapi import FastAPI, HTTPException

from internal.db.models import (
    User,
    UpdateUserChangesetModel,
    UserCollection
)
from internal.db import REPO


app = FastAPI()

@app.post(
    "/users/",
    response_description="Add new user",
    response_model=User,
    status_code=status.CREATED,
    response_model_by_alias=False,
)
async def post_user(user: User):
    return REPO.insert_user(user.model_dump(by_alias=True, exclude=["id"]))

@app.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_users():
    """
    List all of the users data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    # Query params will help to filter
    # Pagination is also pending
    return REPO.get_users()

@app.get(
    "/users/{id}",
    response_description="Get a single user",
    response_model=User,
    response_model_by_alias=False,
)
async def show_user(id: str):
    """
    Get the record for a specific user, looked up by `id`.
    """
    if (user := REPO.get_user(id)) is None:
        raise HTTPException(status_code=status.NOT_FOUND, detail=f"User {id} not found")
    return user


@app.delete(
    "/users/{id}",
    response_description="Delete a single user",
    response_model=User,
    response_model_by_alias=False,
)
async def delete_user(id: str):
    """
    Delete the record for a specific user, looked up by `id`.
    """
    user = REPO.soft_delete_user(id)
    if user is None:
        raise HTTPException(status_code=status.NOT_FOUND, detail=f"User {id} not found")
    return user


@app.put(
    "/users/{id}",
    response_description="Update an user",
    response_model=User,
    response_model_by_alias=False,
)
async def update_user(id: str, user: UpdateUserChangesetModel):
    """
    Update individual fields of an existing user record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    changeset = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }
    return REPO.update_user(id, changeset)
