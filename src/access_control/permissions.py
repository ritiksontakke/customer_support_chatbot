ROLE_TOOLS = {
    "customer": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetTicketChannels",
        "GetTicketsByProduct",
        "GetTicketStatus",
        "deleteTicket",
        

    ],

    "manager": [
        # Read-only (same as customer)
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetTicketChannels",
        "GetTicketsByProduct",
        "GetTicketStatus",
        "deleteTicket",
    ],

    "admin": [
        # Read-only
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "GetTicketChannels",
        "GetTicketsByProduct",
        "GetTicketStatus",

        # Write permissions
        "getCustomerTicket",
        "updateTicket",
        "deleteTicket",
    ],
}