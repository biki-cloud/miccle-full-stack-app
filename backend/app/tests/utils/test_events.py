from sqlmodel import Session

from app.crud import organizers
from app.models import Event, EventCreate
from app.tests.utils.test_users import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_event(db: Session) -> Event:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    title = random_lower_string()
    description = random_lower_string()
    event_in = EventCreate(title=title, description=description)
    return organizers.create_event(session=db, event_in=event_in, owner_id=owner_id)
