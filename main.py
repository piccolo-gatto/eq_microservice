import os
import secrets

from pydantic import EmailStr
from fastapi import FastAPI, UploadFile
from datetime import datetime
from uuid import uuid4

from app.upload_logic import FileStorage

api = FastAPI()

@api.post("/upload_file")
def upload_file(file: UploadFile, user_mail: EmailStr, start_datetime: datetime, end_datetime: datetime): #необходимо реализовать получение токена
	user_id = 0
	#тут будет поиск мейла в бд, если всё в порядке, получаем id пользователя, запоминаем в переменную user_id
	storage = FileStorage()
	token = secrets.token_hex(FileStorage.TOKEN_LENGTH)
	path = storage.make_processing_dir(token)
	#with open(path, "wb") as f:
        #    	f.write(file.read())
	#запись в бд
	return {'status': 'ok', 'user_id': user_id, 'path': path, 'start_datetime': start_datetime, 'end_datetime': end_datetime}