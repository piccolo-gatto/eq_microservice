from pydantic import EmailStr
from fastapi import FastAPI, UploadFile
from uuid import uuid4

#from logic import user_exists, authorisation

api = FastAPI()


@api.post("/register")
async def register(user_name: str, user_mail: EmailStr, password:str):
    token = uuid4()
    #проверка существования в бд
    if user_exists(user_name, user_mail):
        return {"status": "failed", "message":"The user already exists"}
    #добавление
    #
    return {"status":"ok", "user_name": user_name,
            "user_mail": user_mail, "token":token}

@api.post("/log_in")
async def log_in(user_mail: EmailStr, password:str):
    #проверка существования
    #
    #if !authorisation(user_mail,password):
    #    return {"status": "failed", "message":"You are not registered"}
    return {"status":"ok", "token":token}

@api.post("/upload_file")
def upload_file(file: UploadFile): #необходимо реализовать получение токена
	user_id = 0
	#тут будет проверка на корректность токена, если всё в порядке, получаем id пользователя, запоминаем в переменную user_id
	filepath = 'data/' + str(user_id) + '/' + file.filename
	with open(filepath, "wb") as f:
            	f.write(file.read())
	return {'status': 'ok', 'filepath': filepath}