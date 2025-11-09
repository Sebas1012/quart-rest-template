from tortoise import fields, models
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel

class UserLogin(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    create_at = fields.DatetimeField(auto_now_add=True)
    user_rol = fields.CharField(max_length=30, default="Pending")

    def set_password(self, raw_password: str):
        self.password = pbkdf2_sha256.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return pbkdf2_sha256.verify(raw_password, self.password)

class User(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    user_id: int
    user_role: str

class UserResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    message: str