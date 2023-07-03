import app.models as models
import app.crud as crud
from app.database import SessionLocal
from fastapi.testclient import TestClient
import datetime

from app.main import api

client = TestClient(api)
def test_get_last_uploaded():
    test_user = models.User(email="test@example.com")
    test_datetime_start = '2022-01-01 00:00:00'
    test_datetime_end = '2022-01-01 00:10:00'
    db = SessionLocal()
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    test_token = crud.get_ivent_token_by_datetime(db, test_datetime_start, test_datetime_end)
    test_ivent = crud.get_ivent_by_token(db, test_token)
    test_files = [
        models.Uploaded_file(user_id=test_user.id, ivent_id=test_ivent.id,
                             path=str(crud.make_processing_dir(test_token)) + '/' + 'file1.txt',
                             datetime=datetime.datetime(2022, 1, 1, 12, 0, 0)),
        models.Uploaded_file(user_id=test_user.id, ivent_id=test_ivent.id,
                             path=str(crud.make_processing_dir(test_token)) + '/' + 'file2.txt',
                             datetime=datetime.datetime(2022, 1, 1, 14, 30, 0)),
        models.Uploaded_file(user_id=test_user.id, ivent_id=test_ivent.id,
                             path=str(crud.make_processing_dir(test_token)) + '/' + 'file3.txt',
                             datetime=datetime.datetime(2022, 1, 2, 10, 0, 0)),
    ]
    for file in test_files:
        db.add(file)
    db.commit()
    
    response = client.get("/last_uploaded_files/?email=test%40example.com")
    assert response.status_code == 200

    for res in response.json():
        assert res['path'] == str(crud.make_processing_dir(test_token)) + '/' + 'file1.txt' or \
               res['path'] == str(crud.make_processing_dir(test_token)) + '/' + 'file2.txt' or \
               res['path'] == str(crud.make_processing_dir(test_token)) + '/' + 'file3.txt'

    db.delete(test_user)
    for file in test_files:
        db.delete(file)
    db.commit()
    db.close()


def test_get_last_uploaded_files_user_not_found():
    response = client.get("/last_uploaded_files/?email=nonexistent%40example.com")
    
    assert response.status_code != 200
    
    assert response.json() == {"detail": "User not found"}
