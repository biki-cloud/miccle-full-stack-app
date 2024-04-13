from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.crud import organizers
from app.models import Organizer, OrganizerCreate, OrganizerUpdate
from app.tests.utils.utils import random_email, random_lower_string


def organizer_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"organizername": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_organizer(db: Session) -> Organizer:
    email = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=email, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    return organizer


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the organizer with given email.

    If the organizer doesn't exist it is created first.
    """
    password = random_lower_string()
    organizer = organizers.get_organizer_by_email(session=db, email=email)
    if not organizer:
        organizer_in_create = OrganizerCreate(email=email, password=password)
        organizer = organizers.create_organizer(
            session=db, organizer_create=organizer_in_create
        )
    else:
        organizer_in_update = OrganizerUpdate(password=password)
        if not organizer.id:
            raise Exception("Organizer id not set")
        organizer = organizers.update_organizer(
            session=db, db_organizer=organizer, organizer_in=organizer_in_update
        )

    return organizer_authentication_headers(
        client=client, email=email, password=password
    )
