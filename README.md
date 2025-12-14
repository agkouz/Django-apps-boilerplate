# Django Project - Clean Architecture Example

Complete Django project demonstrating the **Services/Selectors pattern** with User and Order management.

## Project Structure

```
django_project/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── pytest.ini                     # Test configuration
│
├── config/                        # Project configuration
│   ├── settings/
│   │   ├── base.py               # Base settings
│   │   ├── development.py        # Development settings
│   │   ├── production.py         # Production settings
│   │   └── test.py               # Test settings
│   ├── urls.py                   # Main URL configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
│
└── apps/                          # Django applications
    ├── core/                      # Shared utilities
    │   ├── models.py             # Base models
    │   └── exceptions.py         # Custom exceptions
    │
    ├── users/                     # User management
    │   ├── models.py             # User model
    │   ├── serializers.py        # DRF serializers
    │   ├── services.py           # Business logic (write)
    │   ├── selectors.py          # Queries (read)
    │   ├── views.py              # API endpoints
    │   ├── urls.py               # URL routing
    │   ├── admin.py              # Django admin
    │   └── tests/                # Tests
    │
    └── orders/                    # Order management
        ├── models.py             # Order model
        ├── serializers.py        # DRF serializers
        ├── services.py           # Business logic (write)
        ├── selectors.py          # Queries (read)
        ├── views.py              # API endpoints
        ├── urls.py               # URL routing
        ├── admin.py              # Django admin
        ├── signals.py            # Event handlers
        └── tests/                # Tests
```

## Architecture Pattern: Services/Selectors

### Layer Breakdown

**Views (API Layer)**
- Handle HTTP requests/responses
- Validate input with DRF serializers
- Call services for write operations
- Call selectors for read operations
- Return serialized responses

**Services (Business Logic - Write)**
- Create, update, delete operations
- Business rule validation
- Orchestrate multiple operations
- Transaction management
- All mutations

**Selectors (Queries - Read)**
- Database queries
- Filtering and aggregation
- Return QuerySets or model instances
- Read-only operations

**Models (Django ORM)**
- Define database schema
- Relationships
- Basic model methods

## Features Demonstrated

### Architecture Patterns
✅ Services/Selectors pattern (Django's clean architecture)
✅ Separation of concerns (views, services, selectors, models)
✅ Business logic in services, not views
✅ Environment-based settings
✅ Django signals for event handling

### Business Logic Examples
✅ Email uniqueness validation
✅ Password hashing
✅ Order total auto-calculation
✅ Quantity limits (max 1000 per order)
✅ Minimum order value ($1.00)
✅ Order status transitions (pending → completed/cancelled)
✅ User statistics aggregation

### Django Features
✅ Custom User model
✅ Django Admin interface
✅ Django REST Framework
✅ Model relationships (User has many Orders)
✅ Django signals
✅ Environment-based configuration
✅ Comprehensive testing

## Setup & Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your settings (defaults work for development)
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

## API Endpoints

### Users

- `POST /api/users/` - Create user
- `GET /api/users/` - List users (with filters)
- `GET /api/users/{id}/` - Get user by ID
- `PUT /api/users/{id}/` - Update user (full)
- `PATCH /api/users/{id}/` - Update user (partial)
- `DELETE /api/users/{id}/` - Delete user

### Orders

- `POST /api/orders/?user_id={user_id}` - Create order
- `GET /api/orders/` - List orders (with filters)
- `GET /api/orders/{id}/` - Get order by ID
- `PUT /api/orders/{id}/` - Update order
- `PATCH /api/orders/{id}/` - Partial update
- `DELETE /api/orders/{id}/` - Delete order
- `POST /api/orders/{id}/complete/` - Mark as completed
- `POST /api/orders/{id}/cancel/` - Cancel order
- `GET /api/orders/user/{user_id}/` - Get user's orders
- `GET /api/orders/user/{user_id}/statistics/` - Get user stats

## Example API Requests

### Create User

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepass123",
    "full_name": "Alice Smith"
  }'
```

### Create Order

```bash
curl -X POST "http://localhost:8000/api/orders/?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Laptop",
    "quantity": 2,
    "unit_price": "999.99"
  }'
```

### Complete Order

```bash
curl -X POST http://localhost:8000/api/orders/1/complete/
```

### Get User Statistics

```bash
curl http://localhost:8000/api/orders/user/1/statistics/
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific app tests
pytest apps/users/tests/
pytest apps/orders/tests/

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest apps/users/tests/test_services.py
```

## Django Admin

Access Django admin at: `http://localhost:8000/admin`

Use the superuser credentials you created to log in.

The admin interface provides:
- User management
- Order management
- Database inspection
- Data entry and editing

## Business Rules Implemented

### User Rules
- Email must be unique
- Password hashed with Django's built-in hasher
- Username synced with email

### Order Rules
- Maximum quantity: 1000 units per order
- Minimum order value: $1.00
- Total amount = quantity × unit_price (auto-calculated)
- Status workflow:
  - `pending` → can transition to `completed` or `cancelled`
  - `completed` → cannot be changed
  - `cancelled` → cannot be changed
- Cannot update completed or cancelled orders
- Cannot delete completed orders
- User must be active to create orders

## Layer-by-Layer Guide

### 1. Models (Database Schema)

Define your database structure:

```python
# apps/users/models.py
class User(AbstractUser, TimestampedModel):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
```

### 2. Serializers (Validation)

Validate API input/output:

```python
# apps/users/serializers.py
class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
```

### 3. Selectors (Read Operations)

Query the database:

```python
# apps/users/selectors.py
def user_get_by_email(*, email: str) -> Optional[User]:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None
```

### 4. Services (Business Logic)

Implement business rules:

```python
# apps/users/services.py
@transaction.atomic
def user_create(*, email: str, password: str) -> User:
    # Check uniqueness
    if user_get_by_email(email=email):
        raise ValidationError("Email exists")
    
    # Create user
    return User.objects.create(email=email, ...)
```

### 5. Views (HTTP Handling)

Handle API requests:

```python
# apps/users/views.py
def create(self, request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = services.user_create(**serializer.validated_data)
    
    return Response(UserSerializer(user).data, status=201)
```

## Key Differences from FastAPI

| Aspect | Django | FastAPI |
|--------|--------|---------|
| **Layers** | Services/Selectors | Single Repository |
| **ORM** | Django ORM (built-in) | SQLAlchemy |
| **Validation** | DRF Serializers | Pydantic |
| **Read/Write** | Split (Selectors/Services) | Combined (Repository) |
| **Admin** | Built-in | Build yourself |
| **Async** | Limited | Native |

## Best Practices

✅ Use `@transaction.atomic` for all service functions
✅ Use keyword-only arguments (`*,`) in services/selectors
✅ Keep views thin - just HTTP handling
✅ Put ALL business logic in services
✅ Use selectors for ALL queries
✅ Never put business logic in serializers or views
✅ Write tests for services and selectors
✅ Use Django admin for internal tools
✅ Follow consistent naming conventions

## Troubleshooting

**Migrations not applying:**
```bash
python manage.py migrate --run-syncdb
```

**Admin not showing custom fields:**
- Check admin.py configuration
- Ensure fieldsets match model fields

**Import errors:**
- Check INSTALLED_APPS in settings
- Ensure app name format is correct (`apps.users`, not `users`)

## Next Steps

1. Add authentication (JWT tokens)
2. Implement permissions (DRF permissions)
3. Add pagination
4. Create more apps (products, payments, etc.)
5. Add caching (Redis)
6. Implement background tasks (Celery)
7. Add API documentation (drf-spectacular)
8. Deploy to production (Gunicorn + Nginx)

## Production Deployment

```bash
# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Use production settings
export DJANGO_SETTINGS_MODULE=config.settings.production
```

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- HackSoft Django Style Guide: https://github.com/HackSoftware/Django-Styleguide
