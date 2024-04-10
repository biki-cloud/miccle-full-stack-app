from sqlmodel import Field, Relationship, SQLModel


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class OrganizerBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superorganizer: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class OrganizerCreate(OrganizerBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class OrganizerCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class OrganizerUpdate(OrganizerBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class OrganizerUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class Organizer(OrganizerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    events: list["Event"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class OrganizerOut(OrganizerBase):
    id: int


class OrganizersOut(SQLModel):
    data: list[OrganizerOut]
    count: int


# Shared properties
class EventBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on event creation
class EventCreate(EventBase):
    title: str


# Properties to receive on event update
class EventUpdate(EventBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(
        default=None, foreign_key="organizer.id", nullable=False
    )
    owner: Organizer | None = Relationship(back_populates="events")


# Properties to return via API, id is always required
class EventOut(EventBase):
    id: int
    owner_id: int


class EventsOut(SQLModel):
    data: list[EventOut]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str
