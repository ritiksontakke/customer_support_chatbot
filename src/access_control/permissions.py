ROLE_TOOLS = {
    "customer": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetChannels",
        "GetProduct",
        "GetTicketStatus",
        "deleteTicket",
        "create_ticket_by_customer",
        

    ],

    "manager": [
        # Read-only (same as customer)
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetChannels",
        "GetProduct",
        "GetTicketStatus",
        "deleteTicket",
    ],

    "admin": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetChannels",
        "GetProduct",
        "GetTicketStatus",

        # Write permissions
        "getCustomerTicket",
        "updateTicket",
        "deleteTicket",
    ],
}