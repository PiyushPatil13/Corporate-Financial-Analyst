from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from app.config import get_settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class AuthService:
    def __init__(self):
        self.settings = get_settings()

    def hash_password(self, plain_password: str) -> str:
        if len(plain_password.encode("utf-8")) > 72:
            raise ValueError("Password cannot exceed 72 bytes")
        
        return pwd_context.hash(plain_password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        if len(plain_password.encode("utf-8")) > 72:
            return False

        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    def create_access_token(self, user_id: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": user_id,
            "exp": expire
        }

        return jwt.encode(
            payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM
        )

    def decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM]
            )

            return payload.get("sub")

        except Exception:
            return None