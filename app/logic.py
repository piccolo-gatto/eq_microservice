from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import secrets

from . import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_id_by_token(db: Session, token: str):
    user = db.query(models.User).filter(models.User.token == token).first()
    return user.id


def generate_token():
    token = secrets.token_hex(16)
    return token

def create_user(db: Session, user: schemas.UserToke):
    token = generate_token()
    db_user = models.User(email=user.email, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
