from peewee import CharField, DateTimeField, TextField, ForeignKeyField
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin

from app.base_model import BaseModel


class Role(BaseModel):
    name = CharField(max_length=100, unique=True, index=True)


class Profile(BaseModel):
    avatar = CharField()
    info = TextField(null=True)


class User(BaseModel, UserMixin):
    username = CharField(max_length=100, index=True)
    email = CharField(max_length=200, unique=True, index=True)
    _password_hash = CharField(max_length=128)
    last_visit = DateTimeField(default=datetime.datetime.now)
    role = ForeignKeyField(Role, backref='users')
    profile = ForeignKeyField(Profile)

    @property
    def password(self):
        raise AttributeError('password is not a valid attribute')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def is_admin(self):
        if self.role.name == 'admin':
            return True
        return False
