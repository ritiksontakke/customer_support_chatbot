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