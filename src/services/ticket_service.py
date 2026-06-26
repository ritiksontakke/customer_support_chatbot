from passlib.context import CryptContext
from datetime import datetime
from src.config.database import SessionLocal
from src.models.customersupport import CustomerSupportTicket
from src.repositories.ticket_repository import TicketRepository
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

class TicketService:

    @staticmethod
    def create_ticket(
        customer_name: str,
        customer_email: str,
        subject: str,
        description: str,
        product: str,
        channel: str,
        priority: str = "Medium",
    ):

        session = SessionLocal()

        try:

            ticket = CustomerSupportTicket(
                customer_name=customer_name,
                customer_email=customer_email,
                product=product,
                category=subject,
                issue_description=description,
                priority=priority,
                status="Open",
                channel=channel,
                ticket_created_date=datetime.utcnow(),
            )

            ticket = TicketRepository.create_ticket(
                db=session,
                ticket=ticket,
            )

            return {
                "success": True,
                "ticket_id": ticket.ticket_id,
                "status": ticket.status,
                "message": "Ticket created successfully.",
            }

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    @staticmethod
    def get_tickets_by_customer_email(
        customer_email: str,
        offset: int = 0,
        limit: int = 5,
    ):

        session = SessionLocal()

        try:
            return TicketRepository.get_tickets_by_customer_email(
                db=session,
                customer_email=customer_email,
                offset=offset,
                limit=limit,
            )

        finally:
            session.close()
    
    @staticmethod
    def get_tickets_by_customer_email_and_status(
        customer_email: str,
        status: str,
        offset: int = 0,
        limit: int = 5,
    ):

        session = SessionLocal()

        try:
            return TicketRepository.get_tickets_by_customer_email_and_status(
                db=session,
                customer_email=customer_email,
                status=status,
                offset=offset,
                limit=limit,
            )

        finally:
            session.close()

    @staticmethod
    def get_tickets_by_channel(
        customer_email: str,
        channel: str,
        offset: int = 0,
        limit: int = 5,
    ):

        session = SessionLocal()

        try:
            return TicketRepository.get_tickets_by_channel(
                db=session,
                customer_email=customer_email,
                channel=channel,
                offset=offset,
                limit=limit,
            )
        finally:
            session.close()

    @staticmethod
    def get_ticket_details(
        ticket_id: int,
        customer_email: str,
    ):

        session = SessionLocal()

        try:
            return TicketRepository.get_ticket_details(
                db=session,
                ticket_id=ticket_id,
                customer_email=customer_email,
            )

        finally:
            session.close()

    @staticmethod
    def get_tickets_by_product(
        customer_email: str,
        product: str,
        offset: int = 0,
        limit: int = 5,
    ):

        session = SessionLocal()

        try:
            return TicketRepository.get_tickets_by_product(
                db=session,
                customer_email=customer_email,
                product=product,
                offset=offset,
                limit=limit,
            )
        finally:
            session.close()

    @staticmethod
    def get_user_role(customer_email: str):

        session = SessionLocal()

        try:
            return TicketRepository.get_user_role(
                db=session,
                customer_email=customer_email,
            )

        finally:
            session.close()
    
    @staticmethod
    def login(customer_email: str):

        session = SessionLocal()

        try:
            return TicketRepository.get_customer_by_email(
                db=session,
                customer_email=customer_email,
            )

        finally:
            session.close()

    @staticmethod
    def signup(
        customer_name: str,
        customer_email: str,
        password: str,
        issue_description:str,
        product:str
    ):

        session = SessionLocal()

        try:

            customer = CustomerSupportTicket(
                customer_name=customer_name,
                customer_email=customer_email,
                issue_description=issue_description,
                product=product,
                hashed_password=pwd_context.hash(password),
                role="Customer",
                status="open",
            )

            TicketRepository.create_customer(
                db=session,
                customer=customer,
            )

            return {
                "message": "User created successfully"
            }

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ):
        return pwd_context.verify(
            plain_password,
            hashed_password,
        )
