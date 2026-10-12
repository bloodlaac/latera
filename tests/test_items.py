import pytest
from datetime import datetime
from backend.api.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from unittest.mock import Mock
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.database.db_connector import DBConnector
from fastapi import status, HTTPException


@pytest.fixture
def new_mock_storage():
    mock_storage = Mock(spec=DBConnector)
    app.dependency_overrides[DBConnector] = lambda: mock_storage

    yield mock_storage

    app.dependency_overrides.pop(DBConnector, None)


@pytest.fixture
def new_client():
    client = TestClient(app)

    return client


def test_add_valid_item(new_mock_storage: Mock, new_client: TestClient):
    item_response = ItemResponse(
        item_id=1,
        title="i'm a title",
        content="item with a title",
        created_at=datetime(2026, 10, 9, 19, 30, 30),
        modified_at=None
    )

    new_mock_storage.add_item.return_value = item_response
    
    new_item = ItemCreate(title="i'm a title", content="item with a title")
    add_response = new_client.post("/items", json=new_item.model_dump())

    assert add_response.status_code == 201
    
    add_response_json = add_response.json()

    assert add_response_json["item_id"] == 1
    assert add_response_json["title"] == "i'm a title"
    assert add_response_json["content"] == "item with a title"
    assert add_response_json["created_at"] == "2026-10-09T19:30:30"
    assert add_response_json["modified_at"] is None

    new_mock_storage.add_item.assert_called_once_with(new_item)


@pytest.mark.parametrize(
    "payload, expected_status", [
        ({"title": "some title", "content": "item with content"}, 201),
        ({"content": "item with content"}, 201),
        ({"title": "some title", "content": ""}, 422),
        ({"title": "some title", "content": "   "}, 422),
        ({"title": "some title"}, 422),
        ({}, 422),
    ]
)
def test_create_item_validation(
    payload: dict,
    expected_status: int,
    new_mock_storage: Mock,
    new_client: TestClient,
):
    item_response = ItemResponse(
        item_id=1,
        title="i'm a title",
        content="item with a title",
        created_at=datetime(2026, 10, 9, 19, 30, 30),
        modified_at=None
    )

    new_mock_storage.add_item.return_value = item_response
    
    response = new_client.post("/items", json=payload)

    assert response.status_code == expected_status

    if expected_status == 201:
        new_mock_storage.add_item.assert_called_once_with(ItemCreate(**payload))
    if expected_status == 422:
        new_mock_storage.add_item.assert_not_called()


def test_select_empty_items(new_mock_storage: Mock, new_client: TestClient):
    new_mock_storage.select_items.return_value = []

    response = new_client.get("/items")

    assert response.status_code == 200
    assert response.json() == []
    new_mock_storage.select_items.assert_called_once_with()


def test_select_non_empty_items(new_mock_storage: Mock, new_client: TestClient):
    first_item = ItemResponse(
        item_id=0,
        title="first",
        content="first item",
        created_at=datetime(2026, 10, 12, 11, 30, 30),
        modified_at=None
    )

    second_item = ItemResponse(
        item_id=1,
        title="second",
        content="second item",
        created_at=datetime(2026, 10, 12, 11, 35, 30),
        modified_at=None
    )

    new_mock_storage.select_items.return_value = [first_item, second_item]

    response = new_client.get("/items")

    assert response.status_code == 200
    assert response.json() == [
        first_item.model_dump(mode="json"),
        second_item.model_dump(mode="json")
    ]
    new_mock_storage.select_items.assert_called_once_with()


def test_select_existing_item(new_mock_storage: Mock, new_client: TestClient):
    item_id = 0
    item_response = ItemResponse(
        item_id=item_id,
        title="first",
        content="first item",
        created_at=datetime(2026, 10, 12, 11, 55, 30),
        modified_at=None
    )

    new_mock_storage.select_item.return_value = item_response
    response = new_client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json() == item_response.model_dump(mode="json")
    new_mock_storage.select_item.assert_called_once_with(item_id)


def test_select_non_existing_item(new_mock_storage: Mock, new_client: TestClient):
    item_id = 1

    new_mock_storage.select_item.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="no item with such id"
    )

    response = new_client.get(f"/items/{item_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "no item with such id"
    new_mock_storage.select_item.assert_called_once_with(item_id)


def test_patch_existing_item(new_mock_storage: Mock, new_client: TestClient):
    item_id = 0
    expected_item = ItemResponse(
        item_id=item_id,
        title="new title",
        content="item with title",
        created_at=datetime(2026, 10, 12, 12, 00, 00),
        modified_at=datetime(2026, 10, 12, 12, 20, 00)
    )
    new_mock_storage.update_item.return_value = expected_item

    updated_item = ItemUpdate(title="new title")
    response = new_client.patch(f"/items/{item_id}", json=updated_item.model_dump(mode="json", exclude_unset=True))

    assert response.status_code == 200
    assert response.json() == expected_item.model_dump(mode="json")
    new_mock_storage.update_item.assert_called_once_with(item_id, updated_item)


def test_patch_non_existing_item(new_mock_storage: Mock, new_client: TestClient):
    item_id = 1
    new_mock_storage.update_item.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="no item with such id"
    )

    updated_item = ItemUpdate(title="new title")
    response = new_client.patch(f"/items/{item_id}", json=updated_item.model_dump(mode="json", exclude_unset=True))

    assert response.status_code == 404
    assert response.json()["detail"] == "no item with such id"
    new_mock_storage.update_item.assert_called_once_with(item_id, updated_item)


@pytest.mark.parametrize(
    "payload", [
        ({"content": None}),
        ({"content": ""}),
        ({"content": "   "}),
    ]
)
def test_update_item_validation(payload, new_mock_storage, new_client):
    item_id = 1
    response = new_client.patch(f"/items/{item_id}", json=payload)
    
    assert response.status_code == 422
    new_mock_storage.update_item.assert_not_called()


def test_delete_existing_item(new_mock_storage: Mock, new_client: TestClient):
    item_id = 0
    new_mock_storage.delete_item.return_value = None
    response = new_client.delete(f"/items/{item_id}")

    assert response.status_code == 204
    assert response.content == b""
    new_mock_storage.delete_item.assert_called_once_with(item_id)


def test_delete_non_existing_item(new_mock_storage: Mock, new_client: TestClient):
    item_id = 1
    new_mock_storage.delete_item.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="no item with such id"
    )

    response = new_client.delete(f"/items/{item_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "no item with such id"
    new_mock_storage.delete_item.assert_called_once_with(item_id)
