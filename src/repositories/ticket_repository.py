from sqlalchemy.orm import Session

from src.models.customersupport import CustomerSupportTicket
from src.models.user import User


class TicketRepository:

    @staticmethod
    def get_tickets_by_customer_email(
        db: Session,
        customer_email: str,
        offset: int = 0,
        limit: int = 5,
    ):
        return (
            db.query(CustomerSupportTicket)
            .join(User, CustomerSupportTicket.user_id == User.id)
            .filter(User.email == customer_email)
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_latest_tickets_by_customer_email(
        db: Session,
        customer_email: str,
        offset: int = 0,
        limit: int = 5,
    ):
        return (
            db.query(CustomerSupportTicket)
            .join(User, CustomerSupportTicket.user_id == User.id)
            .filter(User.email == customer_email)
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_ticket_channels(
        db: Session,
        customer_email: str,
        offset: int = 0,
        limit: int = 5,
    ):
        return (
            db.query(CustomerSupportTicket)
            .join(User, CustomerSupportTicket.user_id == User.id)
            .filter(User.email == customer_email)
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_ticket_details(
        db: Session,
        ticket_id: int | None = None,
        customer_email: str | None = None,
    ):
        query = db.query(CustomerSupportTicket)

        if ticket_id is not None:
            query = query.filter(
                CustomerSupportTicket.ticket_id == ticket_id
            )

        elif customer_email is not None:
            query = (
                query.join(User, CustomerSupportTicket.user_id == User.id)
                .filter(User.email == customer_email)
            )

        if ticket_id is not None:
            return query.first()

        return (
            query.order_by(CustomerSupportTicket.ticket_created_date.desc())
            .limit(5)
            .all()
        )

    @staticmethod
    def get_products(
        db: Session,
        customer_email: str,
        product: str | None = None,
        offset: int = 0,
        limit: int = 5,
    ):
        query = (
            db.query(CustomerSupportTicket)
            .join(User, CustomerSupportTicket.user_id == User.id)
            .filter(User.email == customer_email)
        )

        if product:
            query = query.filter(
                CustomerSupportTicket.product.ilike(f"%{product}%")
            )

        return (
            query.order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_user_role(
        db: Session,
        customer_email: str,
    ):
        user = (
            db.query(User)
            .filter(User.email == customer_email)
            .first()
        )

        if user:
            return user.role

        return None

    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int | None = None,
        customer_email: str | None = None,
        updates: dict | None = None,
    ):
        if updates is None:
            updates = {}

        query = db.query(CustomerSupportTicket)

        if ticket_id is not None:
            query = query.filter(
                CustomerSupportTicket.ticket_id == ticket_id
            )

        elif customer_email is not None:
            query = (
                query.join(User, CustomerSupportTicket.user_id == User.id)
                .filter(User.email == customer_email)
            )

        ticket = query.first()

        if ticket is None:
            return None

        for field, value in updates.items():
            if hasattr(ticket, field):
                setattr(ticket, field, value)

        db.commit()
        db.refresh(ticket)

        return ticket

    @staticmethod
    def delete_ticket(
        db: Session,
        ticket_id: int | None = None,
        customer_email: str | None = None,
    ):
        query = db.query(CustomerSupportTicket)

        if ticket_id is not None:
            query = query.filter(
                CustomerSupportTicket.ticket_id == ticket_id
            )

        elif customer_email is not None:
            query = (
                query.join(User, CustomerSupportTicket.user_id == User.id)
                .filter(User.email == customer_email)
            )

        tickets = query.all()

        if not tickets:
            return 0

        deleted_count = len(tickets)

        for ticket in tickets:
            db.delete(ticket)

        db.commit()

        return deleted_count

    @staticmethod
    def get_active_ticket_by_customer_and_product(
        db: Session,
        customer_email: str,
        product: str,
    ):
        return (
            db.query(CustomerSupportTicket)
            .join(User, CustomerSupportTicket.user_id == User.id)
            .filter(
                User.email == customer_email,
                CustomerSupportTicket.product.ilike(product),
                CustomerSupportTicket.status.in_(
                    ["Open", "Pending", "In Progress"]
                ),
            )
            .first()
        )

    @staticmethod
    def create_ticket(
        db: Session,
        ticket: CustomerSupportTicket,
    ):
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket