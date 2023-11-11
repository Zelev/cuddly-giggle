import json

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.biosignal import (
    create_random_biosignal,
    create_random_biosignal_with_leads_and_insigths,
)


def test_create_biosignal(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    # get client user
    user = crud.user.get_by_email(db, email="client-role@example.com")
    data = {"name": "Foo", "user_id": user.id}
    response = client.post(
        f"{settings.API_V1_STR}/biosignals/",
        headers=client_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = json.loads(response.json())
    assert content["name"] == data["name"]
    assert "id" in content
    assert "user_id" in content


def test_create_biosignal_with_lead(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    # get client user
    user = crud.user.get_by_email(db, email="client-role@example.com")
    data = {
        "name": "Foo",
        "user_id": user.id,
        "leads": [{"name": "Bar", "signal": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}],
    }
    response = client.post(
        f"{settings.API_V1_STR}/biosignals/",
        headers=client_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = json.loads(response.json())
    assert content["name"] == data["name"]
    assert "id" in content
    assert "user_id" in content
    assert len(content["insights"]) == 1
    assert len(content["leads"]) == 1
    # get lead from db
    leads = crud.lead.get_by_biosignal(db, biosignal_id=content["id"])
    assert len(leads) == 1
    for lead in leads:
        assert lead.biosignal_id == content["id"]
        assert lead.name in [_.get("name") for _ in content.get("leads")]
        assert lead.signal in [_.get("signal") for _ in content.get("leads")]


def test_read_biosignal(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    # create biosignal
    user = crud.user.get_by_email(db, email="client-role@example.com")
    biosignal = create_random_biosignal_with_leads_and_insigths(db, user_id=user.id)
    response = client.get(
        f"{settings.API_V1_STR}/biosignals/{biosignal.id}",
        headers=client_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == biosignal.name
    assert content["id"] == biosignal.id
    assert content["user_id"] == biosignal.user_id
    for lead in content["leads"]:
        assert lead["name"] in [_.name for _ in biosignal.leads]
        assert lead["signal"] in [_.signal for _ in biosignal.leads]
    for insight in content["insights"]:
        assert insight["name"] in [_.name for _ in biosignal.insights]
        assert insight["description"] in [_.description for _ in biosignal.insights]


def test_read_biosignals(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # delete all biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    # get client user
    user = crud.user.get_by_email(db, email="client-role@example.com")
    # create biosignals
    biosignal_1 = create_random_biosignal(db, user_id=user.id)
    biosignal_2 = create_random_biosignal(db, user_id=user.id)
    response = client.get(
        f"{settings.API_V1_STR}/biosignals/", headers=client_user_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) > 1
    for content_biosignal in content:
        assert content_biosignal["name"] in [biosignal_1.name, biosignal_2.name]
        assert content_biosignal["id"] in [biosignal_1.id, biosignal_2.id]
        assert content_biosignal["user_id"] in [
            biosignal_1.user_id,
            biosignal_2.user_id,
        ]


def test_update_biosignal(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    # get client user
    user = crud.user.get_by_email(db, email="client-role@example.com")
    biosignal = create_random_biosignal(db, user_id=user.id)
    data = {"name": "Foo", "user_id": biosignal.user_id}
    response = client.put(
        f"{settings.API_V1_STR}/biosignals/{biosignal.id}",
        headers=client_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = json.loads(response.json())
    assert content["name"] == data["name"]
    assert content["id"] == biosignal.id
    assert content["user_id"] == biosignal.user_id


def test_delete_biosignal(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    # get client user
    user = crud.user.get_by_email(db, email="client-role@example.com")
    biosignal = create_random_biosignal(db, user_id=user.id)
    response = client.delete(
        f"{settings.API_V1_STR}/biosignals/{biosignal.id}",
        headers=client_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == biosignal.name
    assert content["id"] == biosignal.id
    assert content["user_id"] == biosignal.user_id
    biosignal = crud.biosignal.get(db, id=biosignal.id)
    assert biosignal is None


def test_get_biosignal_by_user_error(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    biosignal = create_random_biosignal(db)
    response = client.get(
        f"{settings.API_V1_STR}/biosignals/user/{biosignal.user_id}",
        headers=client_user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content is not None


def test_update_biosignal_by_user_error(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    # clean biosignals
    biosignals = crud.biosignal.get_multi(db)
    for biosignal in biosignals:
        crud.biosignal.delete(db, id=biosignal.id)
    biosignal = create_random_biosignal(db)
    data = {"name": "Foo", "user_id": biosignal.user_id}
    response = client.put(
        f"{settings.API_V1_STR}/biosignals/{biosignal.id}",
        headers=client_user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content is not None


def test_delete_biosignal_by_user_error(
    client: TestClient, client_user_token_headers: dict, db: Session
) -> None:
    biosignal = create_random_biosignal(db)
    response = client.delete(
        f"{settings.API_V1_STR}/biosignals/{biosignal.id}",
        headers=client_user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content is not None
