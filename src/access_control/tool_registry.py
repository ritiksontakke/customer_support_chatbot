from src.tools.customer_ticket import get_tickets_by_customer_email
from src.tools.getChannel import getChannel
from src.tools.ticket_details import get_ticket_details
from src.tools.getpoduct import get_product

from src.tools.admin_customer_ticket import get_customer_ticket
from src.tools.get_ticket_status import get_tickets_status
from src.tools.update_ticket import update_ticket
from src.tools.delete_ticket import delete_ticket
from src.tools.create_ticket import create_ticket_by_customer

ALL_TOOLS = {
    get_product.name: get_product,
    get_ticket_details.name: get_ticket_details,
    getChannel.name: getChannel,
    get_tickets_status.name: get_tickets_status,

    get_customer_ticket.name: get_customer_ticket,
    create_ticket_by_customer.name: create_ticket_by_customer,


    update_ticket.name: update_ticket,
    delete_ticket.name: delete_ticket,
}
print(get_product.name)

print(ALL_TOOLS.keys())