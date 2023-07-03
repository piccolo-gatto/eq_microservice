from pydantic import EmailStr
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime, timedelta

from app import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

logger.add("./logs/info.log", retention="1 week")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

@api.post("/upload_file", response_model=schemas.File)
async def upload_file(email: EmailStr, file: UploadFile, type: str, datetime_start: datetime, datetime_end: datetime,
                      db: Session = Depends(get_db)):
    try:
        user = crud.get_user_by_email(db, email=str(email))
        if user:
            user_id = user.id
        else:
            logger.error(f"Email not registred")
            raise HTTPException(status_code=500, detail="Email not registred")
        token = crud.get_ivent_token_by_datetime(db, datetime_start=datetime_start.strftime("%Y-%m-%d %H:%M:%S"),
                                                 datetime_end=datetime_end.strftime("%Y-%m-%d %H:%M:%S"))
        ivent_id = crud.get_ivent_by_token(db, token=token).id
        path = str(crud.make_processing_dir(token)) + '/' + file.filename
        with open(path, "wb") as f:
            f.write(await file.read())
        logger.info(f"{file.filename} File is writing")
        return crud.upload_file(db=db, user_id=user_id, ivent_id=ivent_id, path=path, type=type,
                            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    except:
        logger.error(f"Unprocessable entity")
        raise HTTPException(status_code=422, detail="Unprocessable entity")


@api.get("/last_uploaded_files/", response_model=list[schemas.File])
async def last_uploaded_files(email: EmailStr, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=str(email))
    if not db_user:
        logger.error('User not found')
        raise HTTPException(status_code=400, detail="User not found")
    logger.info('Data received successfully')
    files = crud.get_last_uploaded_files(db=db, user_id=db_user.id)
    return files

@api.get("/files_by_date/", response_model=list[schemas.File])
async def files_by_date(email: EmailStr, date: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        logger.error('User not found')
        raise HTTPException(status_code=400, detail="User not found")

    date_start = datetime.strptime(date, "%Y-%m-%d")
    date_end = date_start + timedelta(days=1)

    files = crud.get_files_by_date(db=db, user_id=db_user.id, date_start=date_start, date_end=date_end)
    return files
