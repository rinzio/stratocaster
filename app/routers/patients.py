from http import HTTPStatus as HTTP

from fastapi import APIRouter, Depends, HTTPException
from typing import Any, List, Dict, Optional

from internal.db.models import PatientModel, PatientChangeset
from internal.db.repository import Patients

# from app.dependencies import get_token_header


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/",
    response_description="Add new patient",
    response_model=PatientModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def post(patient: PatientModel):
    return Patients.create(patient.model_dump(by_alias=True, exclude=["id"]))

@router.get(
    "/",
    response_description="List all patients",
    response_model=List[PatientModel],
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def list(
    id_: Optional[str] = None,
    name: Optional[str] = None,
    p_lastname: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = True
):
    """
    List all of the patients data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    query: Dict[str, Any] = {k: v for k, v in {
        "id": id_,
        "name": name,
        "p_lastname": p_lastname,
        "email": email,
        "is_active": is_active,
    }.items() if v is not None}
    return Patients.list(query)

@router.get(
    "/{id}",
    response_description="Get a single patient",
    response_model=PatientModel,
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def get(id: str, is_active: bool = True):
    """
    Get the record for a specific patient, looked up by `id`.
    """
    if (patient := Patients.get(id, is_active)) is None:
        raise HTTPException(status_code=HTTP.NOT_FOUND, detail=f"Patient {id} not found")
    return patient


@router.delete(
    "/{id}",
    response_description="Delete a single patient",
    response_model=PatientModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def delete(id: str):
    """
    Delete the record for a specific patient, looked up by `id`.
    """
    patient = Patients.delete(id)
    if patient is None:
        raise HTTPException(status_code=HTTP.NOT_FOUND, detail=f"Patient {id} not found")
    return patient


@router.patch(
    "/{id}",
    response_description="Update an patient",
    response_model=PatientModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def update(id: str, patient: PatientChangeset):
    """
    Update individual fields of an existing patient record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    changeset = {
        k: v for k, v in patient.model_dump(by_alias=True).items() if v is not None
    }
    return Patients.update(id, changeset)
