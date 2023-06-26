import pytest
import secrets
from app.logic_storage import (FileStorage, ProcessingDirExists)

class TestStorage():
    
    def test_creation(self):
        storage1 = FileStorage()
        storage2 = FileStorage()
        assert storage1 is storage2
        
    def test_init(self):
        storage = FileStorage()
        storage.init_storage()
        assert storage.init_storage() is False
    
    def test_processing_dir_creation(self):
        storage = FileStorage()
        token = secrets.token_hex(FileStorage.TOKEN_LENGTH)
        info = storage.make_processing_dir(token)
        assert info.is_dir() is True
        
        info = storage.make_processing_dir()
        assert info.is_dir() is True
    
    @pytest.mark.xfail(raises=ProcessingDirExists)
    def test_processing_dir_creation_fails(self):
        storage = FileStorage()
        token = secrets.token_hex(FileStorage.TOKEN_LENGTH)
        storage.make_processing_dir(token)
        storage.make_processing_dir(token)
        
