ROLE_TOOLS = {
    "customer": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetTicketsByChannel",
        "GetTicketsByProduct",
        "GetTicketStatus",
        "deleteTicket",
        

    ],

    "manager": [
        # Read-only (same as customer)
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetTicketsByChannel",
        "GetTicketsByProduct",
        "GetTicketStatus",
        "deleteTicket",
    ],

    "admin": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetTicketsByChannel",
        "GetTicketsByProduct",
        "GetTicketStatus",

        # Write permissions
        "getCustomerTicket",
        "updateTicket",
        "deleteTicket",
    ],
}