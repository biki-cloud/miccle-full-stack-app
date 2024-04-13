from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Event,
    EventCreate,
    Organizer,
    OrganizerCreate,
    OrganizerUpdate,
)


def create_organizer(
    *, session: Session, organizer_create: OrganizerCreate
) -> Organizer:
    db_obj = Organizer.model_validate(
        organizer_create,
        update={"hashed_password": get_password_hash(organizer_create.password)},
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_organizer(
    *, session: Session, db_organizer: Organizer, organizer_in: OrganizerUpdate
) -> Any:
    organizer_data = organizer_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in organizer_data:
        password = organizer_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_organizer.sqlmodel_update(organizer_data, update=extra_data)
    session.add(db_organizer)
    session.commit()
    session.refresh(db_organizer)
    return db_organizer


def get_organizer_by_email(*, session: Session, email: str) -> Organizer | None:
    statement = select(Organizer).where(Organizer.email == email)
    session_organizer = session.exec(statement).first()
    return session_organizer


def authenticate(*, session: Session, email: str, password: str) -> Organizer | None:
    db_organizer = get_organizer_by_email(session=session, email=email)
    if not db_organizer:
        return None
    if not verify_password(password, db_organizer.hashed_password):
        return None
    return db_organizer


def create_event(*, session: Session, event_in: EventCreate, owner_id: int) -> Event:
    db_event = Event.model_validate(event_in, update={"owner_id": owner_id})
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event
