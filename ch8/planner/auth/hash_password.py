from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassowrd:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, password: str, hash: str):
        return pwd_context.verify(password, hash)
