from fastapi.testclient import TestClient
from ..main import app
from ..database.database import Test_session, test_engine, Base
import pytest
from ..routers.cpf import get_db


def override_get_db():
    try:
        db = Test_session()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture(autouse=True)
def create_test_database():
    ("restaurei o banco")
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


def test_create(client):
    response = client.post(
        "/cpf",
        json={
            "cpf": "83609711965"
        })
    assert response.status_code == 201
    assert response.json() == {"message": "Created."}


def test_create_invalid_cpf(client):
    response = client.post(
        "/cpf",
        json={
            "cpf": "12345678910"
        })
    assert response.status_code == 400
    assert response.json() == {"type": "InvalidCpfException",
                               "message": "CPF is not valid."}


def test_create_repeated_cpf(client):
    client.post(
        "/cpf",
        json={
            "cpf": "65139541343"
        })
    response = client.post(
        "/cpf",
        json={
            "cpf": "65139541343"
        })
    assert response.status_code == 409
    assert response.json() == {"type": "ExistsCpfException",
                               "message": "Cpf already exists."}


def test_get_by_cpf(client):
    client.post(
        "/cpf",
        json={
            "cpf": "67666181329"
        })
    response = client.get("/cpf/67666181329")
    assert response.status_code == 200
    assert response.json()["cpf"] == "67666181329"


def test_get_by_invalid_cpf(client):
    response = client.get("/cpf/123567841")
    assert response.status_code == 400
    assert response.json() == {"type": "InvalidCpfException",
                               "message": "CPF is not valid."}


def test_get_by_cpf_not_found(client):
    response = client.get("/cpf/21055699945")
    assert response.status_code == 404
    assert response.json() == {"type": "NotFoundCpfException",
                               "message": "Cpf not found."}


def test_delete(client):
    client.post(
        "/cpf",
        json={
            "cpf": "82224112769"
        })
    response = client.delete("/cpf/82224112769")
    assert response.status_code == 200
    assert response.json() == {"message": "Deleted."}


def test_delete_invalid_cpf(client):
    response = client.get("/cpf/123567841")
    assert response.status_code == 400
    assert response.json() == {"type": "InvalidCpfException",
                               "message": "CPF is not valid."}


def test_delete_cpf_not_found(client):
    response = client.get("/cpf/32727045310")
    assert response.status_code == 404
    assert response.json() == {"type": "NotFoundCpfException",
                               "message": "Cpf not found."}


def test_get_all(client):
    client.post(
        "/cpf",
        json={
            "cpf": "10769148450"
        })
    client.post(
        "/cpf",
        json={
            "cpf": "37385648452"
        })
    response = client.get("/cpf")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2
