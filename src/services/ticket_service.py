from passlib.context import CryptContext
from datetime import datetime
from src.config.database import SessionLocal
from src.models.customersupport import CustomerSupportTicket
from src.repositories.ticket_repository import TicketRepository
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import hashlib
from passlib.exc import UnknownHashError
from typing import Optional
from src.repositories.user_repository import UserRepository

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

            user = UserRepository.get_user_by_email(
                db=session,
                email=customer_email,
            )

            if user is None:
                return {
                    "success": False,
                    "message": "User not found."
                }

            ticket = CustomerSupportTicket(
                user_id=user.id,
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
            return TicketRepository.get_latest_tickets_by_customer_email(
                db=session,
                customer_email=customer_email,
                offset=offset,
                limit=limit,
            
            )
            print(">>> getTicketByCustomerEmail CALLED <<<")
        finally:
            session.close()
    

    @staticmethod
    def get_tickets_by_customer_email_and_status(
        customer_email: str,
        status: Optional[str] = None,
        offset: int = 0,
        limit: int = 5,
    ):
        session = SessionLocal()

        try:
            return TicketRepository.get_latest_tickets_by_customer_email(
                db=session,
                customer_email=customer_email,
                offset=offset,
                limit=limit,
            )

        finally:
            session.close()

    @staticmethod
    def get_ticket_channels(
        customer_email: str,
        offset: int = 0,
        limit: int = 5,
    ):
        session = SessionLocal()
        try:
            return TicketRepository.get_ticket_channels(
                db=session,
                customer_email=customer_email,
                offset=offset,
                limit=limit,
            )
        finally:
            session.close()

    @staticmethod
    def get_ticket_details(
        ticket_id: int | None = None,
        customer_email: str | None = None,
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
    def get_products(
        customer_email: str,
        product: str | None = None,
        offset: int = 0,
        limit: int = 5,
    ):

        session = SessionLocal()

        try:
            return TicketRepository.get_products(
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
    def update_ticket(
        ticket_id: int | None = None,
        customer_email: str | None = None,
        updates: dict | None = None,
    ):

        session = SessionLocal()

        try:

            if updates is None:
                updates = {}

            return TicketRepository.update_ticket(
                db=session,
                ticket_id=ticket_id,
                customer_email=customer_email,
                updates=updates,
            )

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()
    
    @staticmethod
    def delete_ticket(
        ticket_id: int | None = None,
        customer_email: str | None = None,
    ):
        session = SessionLocal()

        try:
            return TicketRepository.delete_ticket(
                db=session,
                ticket_id=ticket_id,
                customer_email=customer_email,
            )
        finally:
            session.close()

    @staticmethod
    def create_ticket_by_customer(
        customer_name: str,
        customer_email: str,
        product: str,
        issue_description: str,
        category: str = "General",
        channel: str = "Chat",
        priority: str = "Medium",
    ):

        session = SessionLocal()

        try:

            # Check existing active ticket
            existing_ticket = TicketRepository.get_active_ticket_by_customer_and_product(
                db=session,
                customer_email=customer_email,
                product=product,
            )

            if existing_ticket:
                return {
                    "success": False,
                    "ticket_id": existing_ticket.ticket_id,
                    "message": (
                        f"You already have an active ticket for '{product}'. "
                        f"Ticket ID: {existing_ticket.ticket_id}."
                    ),
                }
            user = UserRepository.get_user_by_email(
                db=session,
                email=customer_email,
            )

            if user is None:
                return {
                    "success": False,
                    "message": "User not found."
                }

            ticket = CustomerSupportTicket(
                user_id=user.id,
                customer_name=customer_name,
                customer_email=customer_email,
                product=product,
                category=category,
                issue_description=issue_description,
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
