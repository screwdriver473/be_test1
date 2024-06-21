from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select
from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models.models import Patient, PatientOut, PatientsOut, PatientCreate
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.utils import generate_new_account_email, send_email
router = APIRouter()


@router.get(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model= PatientsOut
)
def read_patients(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve patients.
    """

    count_statement = select(func.count()).select_from(Patient)
    count = session.exec(count_statement).one()

    statement = select(Patient).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return PatientsOut(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=PatientOut
)
def create_patient(*, session: SessionDep, patient_in: PatientCreate) -> Any:
    """
    Create new patient.
    """
    patient = crud.get_patient_by_email(session=session, email=patient_in.email)
    if patient:
        raise HTTPException(
            status_code=400,
            detail="The patient with this email already exists in the system.",
        )

    patient = crud.create_patient(session=session, patient_create=patient_in)
    if settings.emails_enabled and patient_in.email:
        email_data = generate_new_account_email(
            email_to=patient_in.email, username=patient_in.email, password=patient_in.password
        )
        send_email(
            email_to=patient_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return patient

@router.get("/{patient_id}", response_model=PatientOut)
def read_patient_by_id(
    patient_id: int, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific patient by pid.
    """
    patient = session.get(Patient, patient_id)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return patient

