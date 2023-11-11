from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.roles import create_random_role
from app.tests.utils.utils import random_lower_string


def test_create_role(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    name = random_lower_string()
    description = random_lower_string()
    data = {"name": name, "description": description}
    r = client.post(
        f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers, json=data
    )
    assert 200 <= r.status_code < 300
    created_role = r.json()
    role = crud.role.get_by_name(db, name=name)
    assert role
    assert role.name == created_role["name"]


def test_read_role_by_name(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    role = create_random_role(db)
    r = client.get(
        f"{settings.API_V1_STR}/roles/{role.name}", headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    api_role = r.json()
    assert api_role
    assert api_role["name"] == role.name


def test_read_roles(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    role = create_random_role(db)
    r = client.get(f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    all_roles = r.json()
    print(all_roles)
    assert role.name in [r["name"] for r in all_roles]


def test_update_role(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    role = create_random_role(db)
    description2 = "updated description"
    data = {"description": description2}
    r = client.put(
        f"{settings.API_V1_STR}/roles/{role.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    updated_role = r.json()
    assert updated_role
    assert updated_role.get("description") == description2
    assert updated_role.get("name") == role.name


def test_delete_role(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    role = create_random_role(db)
    r = client.delete(
        f"{settings.API_V1_STR}/roles/{role.id}", headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    deleted_role = r.json()
    assert deleted_role["name"] == role.name
    role = crud.role.get(db, id=role.id)
    assert not role


def test_delete_role_admin_error(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    # Get admin role
    role = crud.role.get_by_name(db, name="admin")
    r = client.delete(
        f"{settings.API_V1_STR}/roles/{role.id}", headers=normal_user_token_headers
    )
    assert r.status_code == 403


def test_delete_role_not_found_error(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    role = create_random_role(db)
    role_id = role.id
    # delete the role to make sure we will not find it
    crud.role.remove(db, id=role_id)
    r = client.delete(
        f"{settings.API_V1_STR}/roles/{role_id}", headers=superuser_token_headers
    )
    assert r.status_code == 404


def test_create_role_admin_error(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    name = random_lower_string()
    description = random_lower_string()
    data = {"name": name, "description": description}
    r = client.post(
        f"{settings.API_V1_STR}/roles/", headers=normal_user_token_headers, json=data
    )
    assert r.status_code == 403


def test_update_role_admin_error(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    name2 = random_lower_string()
    data = {"name": name2}
    r = client.put(
        f"{settings.API_V1_STR}/roles/{random_lower_string()}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


def test_create_role_existing_name_error(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    role = create_random_role(db)
    name = role.name
    description = random_lower_string()
    data = {"name": name, "description": description}
    r = client.post(
        f"{settings.API_V1_STR}/roles/", headers=superuser_token_headers, json=data
    )
    assert r.status_code == 400


def test_get_role_by_name_error(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    create_random_role(db)
    r = client.get(
        f"{settings.API_V1_STR}/roles/{random_lower_string()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
