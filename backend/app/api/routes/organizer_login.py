from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.organizers import CurrentOrganizer, get_current_active_superorganizer
from app.api.deps.utils import SessionDep
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.crud import organizers
from app.models import Message, NewPassword, Token, OrganizerOut
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/organizer/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    organizer = organizers.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not organizer:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not organizer.is_active:
        raise HTTPException(status_code=400, detail="Inactive organizer")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            organizer.id, expires_delta=access_token_expires
        )
    )


@router.post("/organizer/login/test-token", response_model=OrganizerOut)
def test_token(current_organizer: CurrentOrganizer) -> Any:
    """
    Test access token
    """
    return current_organizer


@router.post("/organizer/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    organizer = organizers.get_organizer_by_email(session=session, email=email)

    if not organizer:
        raise HTTPException(
            status_code=404,
            detail="The organizer with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=organizer.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=organizer.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/organizer/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    organizer = organizers.get_organizer_by_email(session=session, email=email)
    if not organizer:
        raise HTTPException(
            status_code=404,
            detail="The organizer with this email does not exist in the system.",
        )
    elif not organizer.is_active:
        raise HTTPException(status_code=400, detail="Inactive organizer")
    hashed_password = get_password_hash(password=body.new_password)
    organizer.hashed_password = hashed_password
    session.add(organizer)
    session.commit()
    return Message(message="Password updated successfully")


@router.post(
    "/organizer/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superorganizer)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    organizer = organizers.get_organizer_by_email(session=session, email=email)

    if not organizer:
        raise HTTPException(
            status_code=404,
            detail="The organizer with this organizername does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=organizer.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
