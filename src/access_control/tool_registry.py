from src.tools.customer_ticket import get_tickets_by_customer_email
from src.tools.ticket_by_channel import get_tickets_by_channel
from src.tools.ticket_details import get_ticket_details
from src.tools.tickets_by_product import get_tickets_by_product

from src.tools.admin_customer_ticket import get_customer_ticket
from src.tools.get_ticket_status import get_tickets_by_customer_email_and_status
from src.tools.update_ticket import update_ticket
from src.tools.delete_ticket import delete_ticket


ALL_TOOLS = {
    get_tickets_by_customer_email.name: get_tickets_by_customer_email,
    get_ticket_details.name: get_ticket_details,
    get_tickets_by_channel.name: get_tickets_by_channel,
    get_tickets_by_customer_email_and_status.name: get_tickets_by_customer_email_and_status,
    get_tickets_by_product.name: get_tickets_by_product,

    get_customer_ticket.name: get_customer_ticket,

    update_ticket.name: update_ticket,
    delete_ticket.name: delete_ticket,
}