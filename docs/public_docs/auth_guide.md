# Authentication (Public)

Acme API uses Bearer tokens.

Header:
Authorization: Bearer <token>

Tokens are scoped. If a token is missing required scopes, the API returns 403.

Rate limits:
- 60 requests/minute per token
