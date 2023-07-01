import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.database import SessionLocal
import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import api

client = TestClient(api)

class TestUploadFiles():
    
    def test_get_ivent_token_by_datetime(self):
        datetime_start = '2023-05-21 22:34:12'
        datetime_end = '2023-05-21 23:15:08'
        token = crud.generate_token()
        ivent = models.Ivent(datetime_start=datetime_start, datetime_end=datetime_end, token=token)
        db = SessionLocal()
        db.add(ivent)
        db.commit()
        db.refresh(ivent)
        retrieved_token = crud.get_ivent_token_by_datetime(db, datetime_start=datetime_start, datetime_end=datetime_end)
        db.delete(ivent)
        db.commit()
        assert retrieved_token == token


    def test_get_ivent_token_by_datetime_new_datetime(self):
        datetime_start = '2023-03-11 06:01:54'
        datetime_end = '2023-03-11 06:21:33'
        db = SessionLocal()
        retrieved_token = crud.get_ivent_token_by_datetime(db, datetime_start=datetime_start, datetime_end=datetime_end)
        db.delete(crud.get_ivent_by_token(db, token=retrieved_token))
        db.commit()
        assert retrieved_token is not None


    def test_get_ivent_by_token(self):
        datetime_start = '2023-11-12 04:11:47' 
        datetime_end = '2023-11-12 04:15:36'
        token = crud.generate_token()
        ivent = models.Ivent(datetime_start=datetime_start, datetime_end=datetime_end, token=token)
        db = SessionLocal()
        db.add(ivent)
        db.commit()
        db.refresh(ivent)
        retrieved_ivent = crud.get_ivent_by_token(db, token=token)
        db.delete(ivent)
        db.commit()
        assert retrieved_ivent.datetime_start == datetime_start
        assert retrieved_ivent.datetime_end == datetime_end

    def test_api_upload_file(self):
        URL = "/upload_file?email=ekaterina%40gmail.com&type=text&datetime_start=2023-02-03%2000%3A00%3A00&datetime_end=2023-02-03%2006%3A11%3A00"
        file= {'file': ('test.txt', open('./test_files/test.txt', 'rb'), "text/plain")}
        response = client.post(URL, files=file)
        assert response.status_code == 200

    def test_api_upload_file_fail_data(self):
        URL = "/upload_file?email=fail_email%40gmail.com&type=text&datetime_start=2023-02-03%2000%3A00%3A00&datetime_end=2023-02-03%2006%3A11%3A00"
        file = {'file': ('test.txt', open('./test_files/test.txt', 'rb'), "text/plain")}
        response = client.post(URL, files=file)
        assert response.status_code != 200

    def test_api_upload_file_fail_file(self):
        URL = "/upload_file?email=ekaterina%40gmail.com&type=text&datetime_start=2023-02-03%2000%3A00%3A00&datetime_end=2023-02-03%2006%3A11%3A00"
        file = {}
        response = client.post(URL, files=file)
        assert response.status_code != 200

    def test_upload_file(self):
        email = "ekaterina@gmail.com"
        type = 'text'
        datetime_start = '2023-11-12 04:11:47'
        datetime_end = '2023-11-12 04:15:36'
        db = SessionLocal()
        token = crud.get_ivent_token_by_datetime(db, datetime_start=datetime_start, datetime_end=datetime_end)
        user_id = crud.get_user_by_email(db, email=email).id
        ivent_id = crud.get_ivent_by_token(db, token=token).id
        file_name = 'test.txt'
        path = str(crud.make_processing_dir(token)) + '/' + file_name
        new_file = crud.upload_file(db=db, user_id=user_id, ivent_id=ivent_id, path=path, type=type,
                         datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        assert new_file is not None
        assert new_file.path == path
        db.delete(new_file)
        db.commit()


    def test_create_ivent(self):
        datetime_start = '2023-11-12 04:11:47'
        datetime_end = '2023-11-12 04:15:36'
        db = SessionLocal()
        token = crud.get_ivent_token_by_datetime(db, datetime_start=datetime_start, datetime_end=datetime_end)
        new_ivent = crud.create_ivent(db=db, datetime_start=datetime_start, datetime_end=datetime_end, token=token)
        assert new_ivent is not None
        assert new_ivent.token == token
        db.delete(new_ivent)
        db.commit()

    def test_processing_dir(self):
        token = crud.generate_token()
        path = crud.make_processing_dir(token)
        assert path.is_dir() is True
        assert len(token) == crud.TOKEN_LENGTH*2


    def test_processing_dir_fail(self):
        token = ''
        path = crud.make_processing_dir(token)
        assert path.is_dir() is True
        assert len(token) != crud.TOKEN_LENGTH*2