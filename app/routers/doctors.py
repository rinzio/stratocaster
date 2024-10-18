from http import HTTPStatus as HTTP

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Any, List, Dict, Optional

from app.auth.manager import AuthManager
from app.dependencies.dependencies import current_user, is_admin, is_doctor
from internal.db.models.patient import PatientModel
from internal.db.repository import DoctorRepo
from internal.db.models import DoctorModel, DoctorChangeset, DoctorPatientsChangeset


router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
    responses={
        HTTP.CREATED: {"description": "Doctor created"},
        HTTP.BAD_REQUEST: {"description": "Something is wrong with the payload"},
        HTTP.FORBIDDEN: {"description": "Not authorized to use this resource"},
        HTTP.NOT_FOUND: {"description": "Not found"},
    },
)
@router.post(
    "/",
    response_description="Add new doctor",
    response_model=DoctorModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def post(
    doctor: DoctorModel,
    _: Annotated[DoctorModel, Depends(is_admin)],
    ):
    doctor.password = AuthManager.hash(doctor.password)
    return DoctorRepo.create(doctor.model_dump(by_alias=True, exclude=["id"])) # type: ignore

@router.get(
    "/",
    response_description="List all doctors",
    response_model=List[DoctorModel],
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def list(
    _: Annotated[DoctorModel, Depends(is_admin)],
    id_: Optional[str] = None,
    name: Optional[str] = None,
    p_lastname: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = True
):
    """
    List all of the doctors data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    query: Dict[str, Any] = {k: v for k, v in {
        "id": id_,
        "name": name,
        "p_lastname": p_lastname,
        "email": email,
        "is_active": is_active,
    }.items() if v is not None}
    return DoctorRepo.list(query)

@router.get(
    "/{id}",
    response_description="Get a single doctor",
    response_model=DoctorModel,
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def get(id: str, is_active: bool = True):
    """
    Get the record for a specific doctor, looked up by `id`.
    """
    if (doctor := DoctorRepo.get(id=id, is_active=is_active)) is None:
        raise HTTPException(status_code=HTTP.NOT_FOUND, detail=f"Doctor {id} not found")
    return doctor


@router.get(
    "/my/patients",
    response_description="Get patients for a single doctor",
    response_model=List[PatientModel],
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def list_patients(
    _: Annotated[DoctorModel, Depends(is_doctor)],
    current_doctor: Annotated[DoctorModel, Depends(current_user)],
    name: Optional[str] = None,
    p_lastname: Optional[str] = None,
    email: Optional[str] = None,
    limit: int = 1000,
    is_active: bool = True
):
    """
    List all patients for a specific doctor data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    # TODO: Pagination and remove hardcoded 1000
    query: Dict[str, Any] = {k: v for k, v in {
        "name": name,
        "p_lastname": p_lastname,
        "email": email,
        "is_active": is_active,
    }.items() if v is not None}
    try:
        return DoctorRepo.get_patients(str(current_doctor.id), query, limit=limit)
    except RuntimeError as err:
        raise HTTPException(HTTP.NOT_FOUND, detail=str(err))

@router.delete(
    "/{id}",
    response_description="Delete a single doctor",
    response_model=DoctorModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def delete(id: str, _: Annotated[DoctorModel, Depends(is_admin)]):
    """
    Delete the record for a specific doctor, looked up by `id`.
    """
    doctor = DoctorRepo.delete(id)
    if doctor is None:
        raise HTTPException(status_code=HTTP.NOT_FOUND, detail=f"Patient {id} not found")
    return doctor


@router.put(
    "/{id}",
    response_description="Update an doctor",
    response_model=DoctorModel,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def update(id: str, doctor: DoctorChangeset, _: Annotated[DoctorModel, Depends(is_admin)]):
    """
    Update individual fields of an existing doctor record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    changeset = {
        k: v for k, v in doctor.model_dump(by_alias=True).items() if v is not None
    }
    return DoctorRepo.update(id=id, changeset=changeset)


@router.patch(
    "/my/patients",
    response_description="Add patients list",
    response_model=DoctorPatientsChangeset,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def patch(
    changeset: DoctorPatientsChangeset,
    _: Annotated[DoctorModel, Depends(is_doctor)],
    current_doctor: Annotated[DoctorModel, Depends(current_user)]
):
    """
    Add patient(s) to an existing doctor record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    return DoctorRepo.add_patients(changeset.patients, _id=current_doctor.id)


@router.delete(
    "/my/patients",
    response_description="Remove from patients list",
    response_model=DoctorPatientsChangeset,
    status_code=HTTP.CREATED,
    response_model_by_alias=False,
)
async def remove_patients(
    changeset: DoctorPatientsChangeset,
    _: Annotated[DoctorModel, Depends(is_doctor)],
    current_doctor: Annotated[DoctorModel, Depends(current_user)],
):
    """
    Remove patient(s) from an existing doctor record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    return DoctorRepo.remove_patients(changeset.patients, _id=current_doctor.id)


@router.get(
    "/my/patients/stats",
    response_description="Get patient stats",
    status_code=HTTP.OK,
    response_model_by_alias=False,
)
async def get_patient_stats(
    _: Annotated[DoctorModel, Depends(is_doctor)],
    current_doctor: Annotated[DoctorModel, Depends(current_user)],
    ):
    """
    Get patient count for a doctor.
    """
    return DoctorRepo.get_patient_stats(str(current_doctor.id))
