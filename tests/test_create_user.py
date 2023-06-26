import app.logic as logic
import app.models as models
import app.schemas as schemas
from app.database import SessionLocal
import pytest

class TestUserCreation():
    def test_get_user_by_email(self):
        email = "test@example.com"
        user = models.User(email=email)
        db = SessionLocal()
        db.add(user)
        db.commit()
        db.refresh(user)

        retrieved_user = logic.get_user_by_email(db, email=email)
        assert retrieved_user.email == email

    def test_create_user(self):
        email = "test@example.com"
        user = schemas.UserCreate(email=email)
        db = SessionLocal()

        created_user = logic.create_user(db, user=user)
        assert created_user.email == email

        retrieved_user = logic.get_user_by_email(db, email=email)
        assert retrieved_user is not None
        assert retrieved_user.email == email

    
    def test_create_user_fail(self):
        email = "fail"
        user = schemas.UserCreate(email=email)
