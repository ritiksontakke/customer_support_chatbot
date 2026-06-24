# src/permissions.py

ROLE_TOOLS = {
    "customer": [
        "get_tickets_by_customer_email_and_status",
        "get_tickets_by_customer_email",
        "get_ticket_details"
    ],

    "manager": [
        "get_tickets_by_customer_email_and_status",
        "get_tickets_by_customer_email",
        "get_ticket_details",
        "get_tickets_by_channel"
    ],

    "admin": [
        "get_tickets_by_customer_email_and_status",
        "get_tickets_by_customer_email",
        "get_ticket_details",
        "get_tickets_by_channel",
        "get_tickets_by_product"
    ]
}