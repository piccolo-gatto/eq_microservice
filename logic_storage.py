import os
import secrets
import shutil
from pathlib import Path

class ProcessingDirExists(Exception):
    pass

class StorageRootContainsFiles(Exception):
    pass

class ProcessingDirLengthIncorrect(Exception):
    pass


class FileStorage():

    __instance = None
    
    # could import from config.py
    STORAGE_PATH = Path('/eq_data')
    CLEAN_AFTER_SECONDS = 24 * 3600 * 30
    TOKEN_LENGTH = 16

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(FileStorage, cls).__new__(cls)
        return cls.__instance

    def init_storage(self) -> bool:
        if not self.STORAGE_PATH.exists():
            os.makedirs(self.STORAGE_PATH)
            return True
        return False
            
    def make_processing_dir(self, token: str =  None):
        if not token:
            token = secrets.token_hex(self.TOKEN_LENGTH)
        pth = self.STORAGE_PATH / token
        if not pth.exists():
            os.makedirs(pth)
        else:
            raise ProcessingDirExists
        return pth
        
    def validate_storage(self):
        for fname in os.list(self.STORAGE_PATH):
            pth = self.STORAGE_PATH / fname
            if not pth.is_dir():
                raise StorageRootContainsFiles
            else:
                if len(fname) ==self. TOKEN_LENGTH:
                    pass
                else:
                    raise ProcessingDirLengthIncorrect
                
    def clear_storage(self):
        deleted_tokens = []
        for fname in os.list(self.STORAGE_PATH):
            pth = self.STORAGE_PATH / fname
            if time.time() - pth.stat().st_ctime > self.CLEAN_AFTER_SECONDS:
                shutil.rmtree(pth)
                deleted_tokens.append(fname)
        return deleted_tokens
    
    



