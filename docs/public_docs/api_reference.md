# Acme API Reference (Public)

Base URL: https://api.acme.example

## POST /create-order
Creates a new order.

Request JSON:
- order_id (string, required)
- customer_id (string, required)
- items (array, required)
- notes (string, optional)

Max payload size: 256 KB

Responses:
- 201 Created
- 400 Bad Request
- 401 Unauthorized
