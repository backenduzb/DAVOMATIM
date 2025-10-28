from tortoise import fields
from tortoise.models import Model
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    @classmethod
    async def create_user(cls, username: str, password: str, is_admin: bool = False):
        hashed = bcrypt.hash(password)
        return await cls.create(  
            username=username,
            password_hash=hashed,
            is_admin=is_admin
        )
