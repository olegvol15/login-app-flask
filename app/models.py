from flask_login import UserMixin
from datetime import datetime, timedelta
from .extensions import db, login_manager
from .security import EncryptedString, hash_password, check_password

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(EncryptedString, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    locked_until = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = hash_password(password)

    def check_password(self, password):
        return check_password(self.password_hash, password)

    def increment_failed_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=10)

    def reset_failed_attempts(self):
        self.failed_login_attempts = 0
        self.locked_until = None

    def is_account_locked(self):
        if self.locked_until and datetime.utcnow() < self.locked_until:
            return True
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
