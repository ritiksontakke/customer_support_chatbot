from sqlalchemy import Column, BigInteger, Identity, Text
from sqlalchemy.orm import relationship
from src.config.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(
        BigInteger,
        Identity(),
        primary_key=True,
    )

    name = Column(Text, nullable=False)

    email = Column(
        Text,
        unique=True,
        nullable=False
    )

    hashed_password = Column(Text, nullable=False)

    role = Column(
        Text,
        nullable=False,
        default="Customer"
    )

    tickets = relationship(
        "CustomerSupportTicket",
        back_populates="user"
    )