import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.database import SessionLocal
from fastapi.testclient import TestClient

from app.main import api

client = TestClient(api)

class TestUserCreation():
    
    def test_get_user_by_email(self):
        email = "test@example.com"
        user = models.User(email=email)
        db = SessionLocal()
        db.add(user)
        db.commit()
        db.refresh(user)

        retrieved_user = crud.get_user_by_email(db, email=email)
        assert retrieved_user.email == email

    def test_create_user(self):
        email = "test2@example.com"
        user = schemas.UserCreate(email=email)
        db = SessionLocal()

        created_user = crud.create_user(db, user=user)
        assert created_user.email == email

        retrieved_user = crud.get_user_by_email(db, email=email)
        assert retrieved_user is not None
        assert retrieved_user.email == email

    def test_api_create_user(self):
        user = {"email": "example1@example.com"}
        response = client.post("/create_user", json=user)
        assert response.status_code == 200
        assert response.json() == {"email": "example1@example.com"}

    def test_api_create_user_fail(self):
        user = {"email": "example1@example.com"}
        response = client.post("/create_user", json=user)
        assert response.status_code == 400
        assert response.json() == {"detail": "Email already registered"}
