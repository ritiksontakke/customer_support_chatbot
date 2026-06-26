from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Integer,
    Numeric,
    Text,
    TIMESTAMP,
    Identity
)

from src.config.database import Base


class CustomerSupportTicket(Base):
    __tablename__ = "customer_support_tickets"
    __table_args__ = {"schema": "public"}

    ticket_id = Column(
        BigInteger,
        Identity(),
        primary_key=True,
)

    customer_name = Column(Text)
    customer_email = Column(Text)

    product = Column(Text)
    category = Column(Text)
    issue_description = Column(Text)
    resolution_notes = Column(Text)

    priority = Column(Text)
    status = Column(Text)
    channel = Column(Text)

    region = Column(Text)

    customer_age = Column(Integer)
    customer_gender = Column(Text)

    subscription_type = Column(Text)
    customer_tenure_months = Column(Integer)
    previous_tickets = Column(Integer)

    customer_satisfaction_score = Column(Numeric(4, 2))
    first_response_time_hours = Column(Numeric(10, 2))
    resolution_time_hours = Column(Numeric(10, 2))

    ticket_created_date = Column(TIMESTAMP)
    ticket_resolved_date = Column(TIMESTAMP)

    escalated = Column(Boolean)
    sla_breached = Column(Boolean)

    operating_system = Column(Text)
    browser = Column(Text)
    payment_method = Column(Text)
    language = Column(Text)
    preferred_contact_time = Column(Text)

    issue_complexity_score = Column(Numeric(5, 2))

    customer_segment = Column(Text)

    role = Column(Text)

    hashed_password = Column(Text)
    password = Column(Text)