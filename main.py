import os
import secrets

from pydantic import EmailStr
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger
import uvicorn

from app import models, schemas, logic
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


api = FastAPI()


logger.add("./logs/info.log", level="INFO", retention="1 week")


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
async def upload_file(email: EmailStr, file: UploadFile, type: str, datetime_start: datetime, datetime_end: datetime, db: Session = Depends(get_db), response_model=schemas.File):
    #user_id = logic.get_user_by_email(db, email=email) #получается пустой словарь(((
    user_id = 0 #затычка
    ivent_id = 0 #затычка
    #проверка существования события
    #logger.info(f"{token} Token for ivent is getting")
    token = secrets.token_hex(logic.TOKEN_LENGTH)
    logger.info(f"{token} Create new ivent")
    logic.create_ivent(db=db, datetime_start=datetime_start.strftime("%Y-%m-%d %H:%M:%S"), datetime_end=datetime_end.strftime("%Y-%m-%d %H:%M:%S"), token=token)
    path = str(logic.make_processing_dir(token)) + '/' + file.filename
    with open(path, "wb") as f:
        f.write(await file.read())
    logger.info(f"{file.filename} File is writing")
    return logic.upload_file(db=db, user_id=user_id, ivent_id=ivent_id, path=path, type=type, datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    

def main():
    uvicorn.run(f"{os.path.basename(__file__)[:-3]}:api", log_level="info")

if __name__ == '__main__':
    main()