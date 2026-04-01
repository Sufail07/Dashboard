# Dashboard API

Small Django REST API for managing users, roles, financial records, and dashboard summaries.

## Stack

- Django
- Django REST Framework
- Simple JWT
- django-filter
- drf-spectacular
- SQLite by default, PostgreSQL supported via environment variables

## Features

- JWT authentication
- Role-based permissions
- User, role, and financial record management
- Summary endpoints for totals, recent activity, and trends
- Filtering on users and records
- Pagination on list endpoints
- Rate limiting
- OpenAPI schema and Swagger/ReDoc docs

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies.
3. Run migrations.
4. Start the server.

```bash
python manage.py migrate
python manage.py runserver
```

Default local database is SQLite.

## PostgreSQL

To use PostgreSQL, set these environment variables:

```env
DB_ENGINE=postgresql
DB_NAME=dashboard
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_CONN_MAX_AGE=60
```

See [.env.example](/D:/NexoTech/Learning/Dashboard/dashboard/.env.example).

Note: a PostgreSQL driver is required, such as `psycopg[binary]`.

## Auth

- `POST /api/token/`
- `POST /api/token/refresh/`

Use the access token as:

```http
Authorization: Bearer <token>
```

## RBAC

The API uses role-based access control.

- each `User` belongs to a `Role`
- each `Role` stores boolean permission flags
- permissions are enforced in DRF permission classes
- users without authentication are denied
- users without a role are denied
- the `Admin` role is treated as a full-access override

Current permission groups in the system:

- dashboard permissions: `can_view_dashboard`, `can_create_dashboard`, `can_edit_dashboard`, `can_delete_dashboard`
- record permissions: `can_view_record`, `can_create_record`, `can_edit_record`, `can_delete_record`
- summary permissions: `can_view_summary`
- insights flag: `can_access_insights`

Endpoint access is controlled by permission class:

- users and roles endpoints use admin-only access
- records endpoints use record CRUD permissions based on HTTP method
- summary endpoints use summary read permission

For records:

- `GET` requires `can_view_record`
- `POST` requires `can_create_record`
- `PUT/PATCH` requires `can_edit_record`
- `DELETE` requires `can_delete_record`

For summary endpoints:

- `GET` requires `can_view_summary`

## API Docs

- Swagger UI: `/api/docs/swagger/`
- ReDoc: `/api/docs/redoc/`
- OpenAPI schema: `/api/schema/`

## Main Endpoints

- `GET/POST /api/v1/users/`
- `GET/PATCH/DELETE /api/v1/users/{id}/`
- `PATCH /api/v1/users/{id}/toggle/`
- `GET/POST /api/v1/roles/`
- `GET/PATCH/DELETE /api/v1/roles/{id}/`
- `GET/POST /api/v1/records/`
- `GET/PATCH/DELETE /api/v1/records/{id}/`
- `GET /api/v1/summary/total-income/`
- `GET /api/v1/summary/total-expense/`
- `GET /api/v1/summary/net-balance/`
- `GET /api/v1/summary/categories/{category}/`
- `GET /api/v1/summary/recent-activity/`
- `GET /api/v1/summary/trends/?group=weekly`
- `GET /api/v1/summary/trends/?group=monthly`

## Filtering

### Users

- `search`
- `role`
- `is_active`

Example:

```text
/api/v1/users/?search=john&role=Admin&is_active=true
```

### Records

- `category`
- `record_type`
- `user_id`
- `search`
- `date_from`
- `date_to`
- `amount_min`
- `amount_max`

Example:

```text
/api/v1/records/?record_type=expense&category=Food&date_from=2026-04-01&date_to=2026-04-30
```

## Pagination

List endpoints use page-number pagination.

- default page size: `10`
- override with `page_size`
- use `page` for navigation

Example:

```text
/api/v1/records/?page=2&page_size=25
```

## Rate Limits

- anonymous: `30/minute`
- authenticated user: `120/minute`
- login endpoint: `10/minute`
