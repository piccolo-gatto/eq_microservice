from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
import secrets
from loguru import logger

from . import models, schemas

def get_user_by_email(db: Session, email: str):
    try:
        db_user = db.query(models.User).filter(models.User.email == email).first()
    except:
        logger.error("Error receiving user data by email")
        raise HTTPException(status_code=500, detail="Error receiving user data by email")
    return db_user

def get_id_by_token(db: Session, token: str):
    try:
        user = db.query(models.User).filter(models.User.token == token).first()
    except:
        logger.error("Error receiving user data by token")
        raise HTTPException(status_code=500, detail="Error receiving user data by token")
    return user.id

def generate_token():
    logger.info("Generating a token")
    token = secrets.token_hex(16)
    return token

def create_user(db: Session, user: schemas.UserToke):
    token = generate_token()
    db_user = models.User(email=user.email, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"New DB user {db_user.token} was successfully created")
    return db_user
