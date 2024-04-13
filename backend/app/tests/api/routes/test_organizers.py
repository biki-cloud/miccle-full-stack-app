from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.crud import organizers
from app.models import OrganizerCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_organizers_superorganizer_me(
    client: TestClient, superorganizer_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/organizers/me", headers=superorganizer_token_headers
    )
    current_organizer = r.json()
    assert current_organizer
    assert current_organizer["is_active"] is True
    assert current_organizer["is_superorganizer"]
    assert current_organizer["email"] == settings.FIRST_SUPERUSER


def test_get_organizers_normal_organizer_me(
    client: TestClient, normal_organizer_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/organizers/me", headers=normal_organizer_token_headers
    )
    current_organizer = r.json()
    assert current_organizer
    assert current_organizer["is_active"] is True
    assert current_organizer["is_superorganizer"] is False
    assert current_organizer["email"] == settings.EMAIL_TEST_USER


def test_create_organizer_new_email(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    with patch("app.utils.send_email", return_value=None), patch(
        "app.core.config.settings.SMTP_HOST", "smtp.example.com"
    ), patch("app.core.config.settings.SMTP_USER", "admin@example.com"):
        organizername = random_email()
        password = random_lower_string()
        data = {"email": organizername, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/organizers/",
            headers=superorganizer_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_organizer = r.json()
        organizer = organizers.get_organizer_by_email(session=db, email=organizername)
        assert organizer
        assert organizer.email == created_organizer["email"]


def test_get_existing_organizer(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    organizer_id = organizer.id
    r = client.get(
        f"{settings.API_V1_STR}/organizers/{organizer_id}",
        headers=superorganizer_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_organizer = r.json()
    existing_organizer = organizers.get_organizer_by_email(
        session=db, email=organizername
    )
    assert existing_organizer
    assert existing_organizer.email == api_organizer["email"]


def test_get_existing_organizer_current_organizer(
    client: TestClient, db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    organizer_id = organizer.id

    login_data = {
        "organizername": organizername,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.get(
        f"{settings.API_V1_STR}/organizers/{organizer_id}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_organizer = r.json()
    existing_organizer = organizers.get_organizer_by_email(
        session=db, email=organizername
    )
    assert existing_organizer
    assert existing_organizer.email == api_organizer["email"]


def test_get_existing_organizer_permissions_error(
    client: TestClient, normal_organizer_token_headers: dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/organizers/999999",
        headers=normal_organizer_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "The organizer doesn't have enough privileges"}


def test_create_organizer_existing_organizername(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    # organizername = email
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizers.create_organizer(session=db, organizer_create=organizer_in)
    data = {"email": organizername, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/organizers/",
        headers=superorganizer_token_headers,
        json=data,
    )
    created_organizer = r.json()
    assert r.status_code == 400
    assert "_id" not in created_organizer


def test_create_organizer_by_normal_organizer(
    client: TestClient, normal_organizer_token_headers: dict[str, str]
) -> None:
    organizername = random_email()
    password = random_lower_string()
    data = {"email": organizername, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/organizers/",
        headers=normal_organizer_token_headers,
        json=data,
    )
    assert r.status_code == 400


def test_retrieve_organizers(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizers.create_organizer(session=db, organizer_create=organizer_in)

    organizername2 = random_email()
    password2 = random_lower_string()
    organizer_in2 = OrganizerCreate(email=organizername2, password=password2)
    organizers.create_organizer(session=db, organizer_create=organizer_in2)

    r = client.get(
        f"{settings.API_V1_STR}/organizers/", headers=superorganizer_token_headers
    )
    all_organizers = r.json()

    assert len(all_organizers["data"]) > 1
    assert "count" in all_organizers
    for item in all_organizers["data"]:
        assert "email" in item


def test_update_organizer_me(
    client: TestClient, normal_organizer_token_headers: dict[str, str], db: Session
) -> None:
    full_name = "Updated Name"
    email = random_email()
    data = {"full_name": full_name, "email": email}
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/me",
        headers=normal_organizer_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_organizer = r.json()
    assert updated_organizer["email"] == email
    assert updated_organizer["full_name"] == full_name


def test_update_password_me(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": new_password,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/me/password",
        headers=superorganizer_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_organizer = r.json()
    assert updated_organizer["message"] == "Password updated successfully"

    # Revert to the old password to keep consistency in test
    old_data = {
        "current_password": new_password,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/me/password",
        headers=superorganizer_token_headers,
        json=old_data,
    )
    assert r.status_code == 200


def test_update_password_me_incorrect_password(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {"current_password": new_password, "new_password": new_password}
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/me/password",
        headers=superorganizer_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_organizer = r.json()
    assert updated_organizer["detail"] == "Incorrect password"


def test_update_organizer_me_email_exists(
    client: TestClient, normal_organizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)

    data = {"email": organizer.email}
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/me",
        headers=normal_organizer_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "Organizer with this email already exists"


def test_update_password_me_same_password_error(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/me/password",
        headers=superorganizer_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_organizer = r.json()
    assert (
        updated_organizer["detail"]
        == "New password cannot be the same as the current one"
    )


def test_create_organizer_open(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        organizername = random_email()
        password = random_lower_string()
        full_name = random_lower_string()
        data = {"email": organizername, "password": password, "full_name": full_name}
        r = client.post(
            f"{settings.API_V1_STR}/organizers/open",
            json=data,
        )
        assert r.status_code == 200
        created_organizer = r.json()
        assert created_organizer["email"] == organizername
        assert created_organizer["full_name"] == full_name


def test_create_organizer_open_forbidden_error(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", False):
        organizername = random_email()
        password = random_lower_string()
        full_name = random_lower_string()
        data = {"email": organizername, "password": password, "full_name": full_name}
        r = client.post(
            f"{settings.API_V1_STR}/organizers/open",
            json=data,
        )
        assert r.status_code == 403
        assert (
            r.json()["detail"]
            == "Open organizer registration is forbidden on this server"
        )


def test_create_organizer_open_already_exists_error(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        password = random_lower_string()
        full_name = random_lower_string()
        data = {
            "email": settings.FIRST_SUPERUSER,
            "password": password,
            "full_name": full_name,
        }
        r = client.post(
            f"{settings.API_V1_STR}/organizers/open",
            json=data,
        )
        assert r.status_code == 400
        assert (
            r.json()["detail"]
            == "The organizer with this email already exists in the system"
        )


def test_update_organizer(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)

    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/{organizer.id}",
        headers=superorganizer_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_organizer = r.json()
    assert updated_organizer["full_name"] == "Updated_full_name"


def test_update_organizer_not_exists(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/99999999",
        headers=superorganizer_token_headers,
        json=data,
    )
    assert r.status_code == 404
    assert (
        r.json()["detail"] == "The organizer with this id does not exist in the system"
    )


def test_update_organizer_email_exists(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)

    organizername2 = random_email()
    password2 = random_lower_string()
    organizer_in2 = OrganizerCreate(email=organizername2, password=password2)
    organizer2 = organizers.create_organizer(session=db, organizer_create=organizer_in2)

    data = {"email": organizer2.email}
    r = client.patch(
        f"{settings.API_V1_STR}/organizers/{organizer.id}",
        headers=superorganizer_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "Organizer with this email already exists"


def test_delete_organizer_super_organizer(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    organizer_id = organizer.id
    r = client.delete(
        f"{settings.API_V1_STR}/organizers/{organizer_id}",
        headers=superorganizer_token_headers,
    )
    assert r.status_code == 200
    deleted_organizer = r.json()
    assert deleted_organizer["message"] == "Organizer deleted successfully"


def test_delete_organizer_current_organizer(client: TestClient, db: Session) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)
    organizer_id = organizer.id

    login_data = {
        "organizername": organizername,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.delete(
        f"{settings.API_V1_STR}/organizers/{organizer_id}",
        headers=headers,
    )
    assert r.status_code == 200
    deleted_organizer = r.json()
    assert deleted_organizer["message"] == "Organizer deleted successfully"


def test_delete_organizer_not_found(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/organizers/99999999",
        headers=superorganizer_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Organizer not found"


def test_delete_organizer_current_super_organizer_error(
    client: TestClient, superorganizer_token_headers: dict[str, str], db: Session
) -> None:
    super_organizer = organizers.get_organizer_by_email(
        session=db, email=settings.FIRST_SUPERUSER
    )
    assert super_organizer
    organizer_id = super_organizer.id

    r = client.delete(
        f"{settings.API_V1_STR}/organizers/{organizer_id}",
        headers=superorganizer_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "Super organizers are not allowed to delete themselves"


def test_delete_organizer_without_privileges(
    client: TestClient, normal_organizer_token_headers: dict[str, str], db: Session
) -> None:
    organizername = random_email()
    password = random_lower_string()
    organizer_in = OrganizerCreate(email=organizername, password=password)
    organizer = organizers.create_organizer(session=db, organizer_create=organizer_in)

    r = client.delete(
        f"{settings.API_V1_STR}/organizers/{organizer.id}",
        headers=normal_organizer_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The organizer doesn't have enough privileges"
