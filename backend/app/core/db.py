from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.crud import organizers, users
from app.models import Organizer, OrganizerCreate, User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel model are imported (app.model) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the model are already imported and registered from app.model
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = users.create_user(session=session, user_create=user_in)

    organizer = session.exec(
        select(Organizer).where(Organizer.email == settings.FIRST_SUPERUSER)
    ).first()
    if not organizer:
        organizer_in = OrganizerCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superorganizer=True,
        )
        organizer = organizers.create_organizer(
            session=session, organizer_create=organizer_in
        )
