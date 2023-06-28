from pydantic import EmailStr
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

logger.add("./logs/info.log", retention="1 week")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Endpoints
@api.post("/create_user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("Received request to create a user")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.info(f"Email {db_user.token} already registered")
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db=db, user=user)
    logger.info(f"User {created_user.token} created successfully")
    return created_user
