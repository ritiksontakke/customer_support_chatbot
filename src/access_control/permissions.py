ROLE_TOOLS = {
    "customer": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "getTicketsByChannel",
        "getTicketsByProduct",
    ],

    "manager": [
        # Read-only (same as customer)
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "getTicketsByChannel",
        "getTicketsByProduct",
    ],

    "admin": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "getTicketsByChannel",
        "getTicketsByProduct",

        # Write permissions
        "getCustomerTicket",
        "updateTicket",
        "deleteTicket",
    ],
}