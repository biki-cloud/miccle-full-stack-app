from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError

from app.api.deps.utils import SessionDep, TokenDep
from app.core import security
from app.core.config import settings
from app.model.organizers import Organizer, TokenPayload


def get_current_organizer(session: SessionDep, token: TokenDep) -> Organizer:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    organizer = session.get(Organizer, token_data.sub)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    if not organizer.is_active:
        raise HTTPException(status_code=400, detail="Inactive organizer")
    return organizer


CurrentOrganizer = Annotated[Organizer, Depends(get_current_organizer)]


def get_current_active_superorganizer(current_organizer: CurrentOrganizer) -> Organizer:
    if not current_organizer.is_superorganizer:
        raise HTTPException(
            status_code=400, detail="The organizer doesn't have enough privileges"
        )
    return current_organizer
