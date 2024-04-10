from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app.core.security import verify_password
from app.crud import organizers
from app.model.organizers import Organizer, OrganizerCreate, OrganizerUpdate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_organizer(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=email, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    assert organizer.email == email
    assert hasattr(organizer, "hashed_password")


def test_authenticate_organizer(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=email, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    authenticated_organizer = organizers.authenticate(
        session=db, email=email, password=password
    )
    assert authenticated_organizer
    assert organizer.email == authenticated_organizer.email


def test_not_authenticate_organizer(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organizer = organizers.authenticate(session=db, email=email, password=password)
    assert organizer is None


def test_check_if_organizer_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=email, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    assert organizer.is_active is True


def test_check_if_organizer_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=email, password=password, disabled=True)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    assert organizer.is_active


def test_check_if_organizer_is_superorganizer(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(
        email=email, password=password, is_superorganizer=True
    )
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    assert organizer.is_superorganizer is True


def test_check_if_organizer_is_superorganizer_normal_organizer(db: Session) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    assert organizer.is_superorganizer is False


def test_get_organizer(db: Session) -> None:
    password = random_lower_string()
    organizername = random_email()
    organizer_in = OrganizerCreate(
        email=organizername, password=password, is_superorganizer=True
    )
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    organizer_2 = db.get(Organizer, organizer.id)
    assert organizer_2
    assert organizer.email == organizer_2.email
    assert jsonable_encoder(organizer) == jsonable_encoder(organizer_2)


def test_update_organizer(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    organizer_in = OrganizerCreate(
        email=email, password=password, is_superorganizer=True
    )
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    new_password = random_lower_string()
    organizer_in_update = OrganizerUpdate(password=new_password, is_superorganizer=True)
    if organizer.id is not None:
        organizers.update_organizer(
            session=db, db_organizer=organizer, organizer_in=organizer_in_update
        )
    organizer_2 = db.get(Organizer, organizer.id)
    assert organizer_2
    assert organizer.email == organizer_2.email
    assert verify_password(new_password, organizer_2.hashed_password)
