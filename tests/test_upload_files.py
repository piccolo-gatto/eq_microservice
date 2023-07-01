import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.database import SessionLocal
import pytest
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
        assert retrieved_token != None


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

    def test_api_upload_file_fail_email(self):
        URL = "/upload_file?email=fail_email%40gmail.com&type=text&datetime_start=2023-02-03%2000%3A00%3A00&datetime_end=2023-02-03%2006%3A11%3A00"
        file = {'file': ('test.txt', open('./test_files/test.txt', 'rb'), "text/plain")}
        response = client.post(URL, files=file)
        assert response.status_code != 200

    def test_api_upload_file_fail_file(self):
        URL = "/upload_file?email=ekaterina%40gmail.com&type=text&datetime_start=2023-02-03%2000%3A00%3A00&datetime_end=2023-02-03%2006%3A11%3A00"
        file = {}
        response = client.post(URL, files=file)
        assert response.status_code != 200

    