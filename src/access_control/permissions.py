# src/permissions.py

# src/access_control/permissions.py

ROLE_TOOLS = {
    "customer": [
        "getTicketByCustomerEmail",
        "getTicketByCustomerEmailAndStatus",
        "getTicketDetails",
        "getTicketsByChannel",
        "getTicketsByProduct",
    ],

    "manager": [
        # Manager read tools will be added later
    ],

    "admin": [
        # Admin read/write tools will be added later
    ]
}
# # src/permissions.py

# ROLE_TOOLS = {
#     "customer": [
#         "get_tickets_by_customer_email_and_status",
#         "get_tickets_by_customer_email",
#         "get_ticket_details"
#     ],

#     "manager": [
#         "get_tickets_by_customer_email_and_status",
#         "get_tickets_by_customer_email",
#         "get_ticket_details",
#         "get_tickets_by_channel"
#     ],

#     "admin": [
#         "get_tickets_by_customer_email_and_status",
#         "get_tickets_by_customer_email",
#         "get_ticket_details",
#         "get_tickets_by_channel",
#         "get_tickets_by_product"
#     ]
# }