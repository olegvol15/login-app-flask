import os
import bcrypt
from cryptography.fernet import Fernet
from sqlalchemy.types import TypeDecorator, LargeBinary

FERNET_KEY = os.environ.get("FERNET_KEY", "")
if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY missing")
fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def check_password(hashed: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

class EncryptedString(TypeDecorator):
    impl = LargeBinary
    cache_ok = True
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return fernet.encrypt(value.encode("utf-8"))
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return fernet.decrypt(value).decode("utf-8")
