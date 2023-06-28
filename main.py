import os
import secrets

from pydantic import EmailStr
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger

from app.logic_storage import FileStorage
from app import models, schemas, logic
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


api = FastAPI()


logger.add("./logs/info.log", level="INFO")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api.post("/create_user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = logic.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #добавление
    return logic.create_user(db=db, user=user)


@api.post(f"/upload_file")
def upload_file(file: UploadFile, datetime: schemas.IventCreate, db: Session = Depends(get_db)):
	#получение юзера
	user_id = 0
	storage = FileStorage()
	#проверка существования даты
	logger.info(f"{token} Token for ivent is getting")
	logger.info(f"{token} Create new ivent")
	token = secrets.token_hex(FileStorage.TOKEN_LENGTH)
	logic.create_ivent(db=db, datetime=datetime, token=token)
	path = str(storage.make_processing_dir(token) / file.filename)
	with open(path, "w") as f:
		logger.info(f"{file.filename} File is writing")
          	f.write('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
	return logic.upload_file(db=db, user_id=user_id, path=path)