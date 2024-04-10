from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app.api.deps.organizers import (
    CurrentOrganizer,
    get_current_active_superorganizer,
)
from app.api.deps.utils import SessionDep
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.crud import organizers
from app.model.organizers import (
    Event,
    Message,
    Organizer,
    OrganizerCreate,
    OrganizerCreateOpen,
    OrganizerOut,
    OrganizersOut,
    OrganizerUpdate,
    OrganizerUpdateMe,
    UpdatePassword,
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superorganizer)],
    response_model=OrganizersOut,
)
def read_organizers(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve organizers.
    """

    count_statement = select(func.count()).select_from(Organizer)
    count = session.exec(count_statement).one()

    statement = select(Organizer).offset(skip).limit(limit)
    organizers = session.exec(statement).all()

    return OrganizersOut(data=organizers, count=count)


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superorganizer)],
    response_model=OrganizerOut,
)
def create_organizer(*, session: SessionDep, organizer_in: OrganizerCreate) -> Any:
    """
    Create new organizer.
    """
    organizer = organizers.get_organizer_by_email(
        session=session, email=organizer_in.email
    )
    if organizer:
        raise HTTPException(
            status_code=400,
            detail="The organizer with this email already exists in the system.",
        )

    organizer = organizers.create_organizer(
        session=session, organizer_create=organizer_in
    )
    if settings.emails_enabled and organizer_in.email:
        email_data = generate_new_account_email(
            email_to=organizer_in.email,
            username=organizer_in.email,
            password=organizer_in.password,
        )
        send_email(
            email_to=organizer_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return organizer


@router.patch("/me", response_model=OrganizerOut)
def update_organizer_me(
    *,
    session: SessionDep,
    organizer_in: OrganizerUpdateMe,
    current_organizer: CurrentOrganizer,
) -> Any:
    """
    Update own organizer.
    """

    if organizer_in.email:
        existing_organizer = organizers.get_organizer_by_email(
            session=session, email=organizer_in.email
        )
        if existing_organizer and existing_organizer.id != current_organizer.id:
            raise HTTPException(
                status_code=409, detail="Organizer with this email already exists"
            )
    organizer_data = organizer_in.model_dump(exclude_unset=True)
    current_organizer.sqlmodel_update(organizer_data)
    session.add(current_organizer)
    session.commit()
    session.refresh(current_organizer)
    return current_organizer


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_organizer: CurrentOrganizer
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_organizer.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_organizer.hashed_password = hashed_password
    session.add(current_organizer)
    session.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=OrganizerOut)
def read_organizer_me(session: SessionDep, current_organizer: CurrentOrganizer) -> Any:
    """
    Get current organizer.
    """
    return current_organizer


@router.post("/open", response_model=OrganizerOut)
def create_organizer_open(
    session: SessionDep, organizer_in: OrganizerCreateOpen
) -> Any:
    """
    Create new organizer without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open organizer registration is forbidden on this server",
        )
    organizer = organizers.get_organizer_by_email(
        session=session, email=organizer_in.email
    )
    if organizer:
        raise HTTPException(
            status_code=400,
            detail="The organizer with this email already exists in the system",
        )
    organizer_create = OrganizerCreate.from_orm(organizer_in)
    organizer = organizers.create_organizer(
        session=session, organizer_create=organizer_create
    )
    return organizer


@router.get("/{organizer_id}", response_model=OrganizerOut)
def read_organizer_by_id(
    organizer_id: int, session: SessionDep, current_organizer: CurrentOrganizer
) -> Any:
    """
    Get a specific organizer by id.
    """
    organizer = session.get(Organizer, organizer_id)
    if organizer == current_organizer:
        return organizer
    if not current_organizer.is_superorganizer:
        raise HTTPException(
            status_code=403,
            detail="The organizer doesn't have enough privileges",
        )
    return organizer


@router.patch(
    "/{organizer_id}",
    dependencies=[Depends(get_current_active_superorganizer)],
    response_model=OrganizerOut,
)
def update_organizer(
    *,
    session: SessionDep,
    organizer_id: int,
    organizer_in: OrganizerUpdate,
) -> Any:
    """
    Update a organizer.
    """

    db_organizer = session.get(Organizer, organizer_id)
    if not db_organizer:
        raise HTTPException(
            status_code=404,
            detail="The organizer with this id does not exist in the system",
        )
    if organizer_in.email:
        existing_organizer = organizers.get_organizer_by_email(
            session=session, email=organizer_in.email
        )
        if existing_organizer and existing_organizer.id != organizer_id:
            raise HTTPException(
                status_code=409, detail="Organizer with this email already exists"
            )

    db_organizer = organizers.update_organizer(
        session=session, db_organizer=db_organizer, organizer_in=organizer_in
    )
    return db_organizer


@router.delete("/{organizer_id}")
def delete_organizer(
    session: SessionDep, current_organizer: CurrentOrganizer, organizer_id: int
) -> Message:
    """
    Delete a organizer.
    """
    organizer = session.get(Organizer, organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    elif organizer != current_organizer and not current_organizer.is_superorganizer:
        raise HTTPException(
            status_code=403, detail="The organizer doesn't have enough privileges"
        )
    elif organizer == current_organizer and current_organizer.is_superorganizer:
        raise HTTPException(
            status_code=403,
            detail="Super organizers are not allowed to delete themselves",
        )

    statement = delete(Event).where(col(Event.owner_id) == organizer_id)
    session.exec(statement)  # type: ignore
    session.delete(organizer)
    session.commit()
    return Message(message="Organizer deleted successfully")
