from sqlalchemy.orm import Session

from src.models.customersupport import CustomerSupportTicket


class TicketRepository:

    @staticmethod
    def create_ticket(
        db: Session,
        ticket: CustomerSupportTicket,
    ) -> CustomerSupportTicket:

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket
    
    @staticmethod
    def get_tickets_by_customer_email(
        db: Session,
        customer_email: str,
        offset: int = 0,
        limit: int = 5,
    ):

        return (
            db.query(CustomerSupportTicket)
            .filter(CustomerSupportTicket.customer_email == customer_email)
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_tickets_by_customer_email_and_status(
        db: Session,
        customer_email: str,
        status: str,
        offset: int = 0,
        limit: int = 5,
    ):

        return (
            db.query(CustomerSupportTicket)
            .filter(
                CustomerSupportTicket.customer_email == customer_email,
                CustomerSupportTicket.status == status,
            )
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_tickets_by_channel(
        db: Session,
        customer_email: str,
        channel: str,
        offset: int = 0,
        limit: int = 5,
    ):

        return (
            db.query(CustomerSupportTicket)
            .filter(
                CustomerSupportTicket.customer_email == customer_email,
                CustomerSupportTicket.channel == channel,
            )
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    

    @staticmethod
    def get_ticket_details(
        db: Session,
        ticket_id: int,
        customer_email: str,
    ):

        return (
            db.query(CustomerSupportTicket)
            .filter(
                CustomerSupportTicket.ticket_id == ticket_id,
                CustomerSupportTicket.customer_email == customer_email,
            )
            .first()
        )
    
    @staticmethod
    def get_tickets_by_product(
        db: Session,
        customer_email: str,
        product: str,
        offset: int = 0,
        limit: int = 5,
    ):

        return (
            db.query(CustomerSupportTicket)
            .filter(
                CustomerSupportTicket.customer_email == customer_email,
                CustomerSupportTicket.product == product,
            )
            .order_by(CustomerSupportTicket.ticket_created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_user_role(
        db: Session,
        customer_email: str,
    ):

        ticket = (
            db.query(CustomerSupportTicket)
            .filter(CustomerSupportTicket.customer_email == customer_email)
            .first()
        )

        if ticket:
            return ticket.role

        return None

    @staticmethod
    def get_customer_by_email(
        db: Session,
        customer_email: str,
    ):
        return (
            db.query(CustomerSupportTicket)
            .filter(
                CustomerSupportTicket.customer_email == customer_email
            )
            .first()
        )

    @staticmethod
    def create_customer(
        db: Session,
        customer: CustomerSupportTicket,
    ):

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

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
            query = query.filter(
                CustomerSupportTicket.customer_email == customer_email
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
            query = query.filter(
                CustomerSupportTicket.customer_email == customer_email
            )

        tickets = query.all()

        if not tickets:
            return 0

        deleted_count = len(tickets)

        for ticket in tickets:
            db.delete(ticket)

        db.commit()

        return deleted_count