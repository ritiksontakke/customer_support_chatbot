from passlib.context import CryptContext
from src.config.database import SessionLocal
from src.models.user import User
from src.repositories.user_repository import UserRepository
import hashlib
from passlib.exc import UnknownHashError

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class UserService:

    @staticmethod
    def signup(
        customer_name: str,
        customer_email: str,
        password: str,
    ):

        session = SessionLocal()

        try:

            # Check if user already exists
            existing_user = UserRepository.get_user_by_email(
                db=session,
                email=customer_email,
            )

            if existing_user:
                return {
                    "success": False,
                    "message": "Email already registered."
                }

            user = User(
                name=customer_name,
                email=customer_email,
                hashed_password=pwd_context.hash(password),
                role="Customer",
            )

            UserRepository.create_user(
                db=session,
                user=user,
            )

            return {
                "success": True,
                "message": "User created successfully."
            }

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    @staticmethod
    def login(
        customer_email: str,
    ):

        session = SessionLocal()

        try:

            return UserRepository.get_user_by_email(
                db=session,
                email=customer_email,
            )

        finally:
            session.close()

    @staticmethod
    def verify_password(
        plain_password: str,
        stored_password: str,
    ):
        # Plain password
        if plain_password == stored_password:
            return True

        # SHA256 password
        sha256_hash = hashlib.sha256(
            plain_password.encode()
        ).hexdigest()

        if sha256_hash == stored_password:
            return True

        # bcrypt password
        try:
            return pwd_context.verify(
                plain_password,
                stored_password,
            )
        except UnknownHashError:
            return False