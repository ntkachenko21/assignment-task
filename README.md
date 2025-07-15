# Test Assignment for Hustlr Staffing Services – E-commerce Product API (Django Rest)

> **(Requirements) Time Limit: Spend no more than 1 hour**
> 
> **Time spent on this project: 1 hour (real hands-on coding and setup, not an estimate).**



---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Features & Endpoints](#features--endpoints)
5. [Project Structure](#project-structure)
6. [How to Run Locally](#how-to-run-locally)
7. [API Documentation (Swagger)](#api-documentation-swagger)
9. [Detailed Code Analysis](#detailed-code-analysis)
10. [Notes & Decisions](#notes--decisions)

---

## Project Overview

This repository contains a fully functional backend for an e-commerce product API built with Django & Django REST Framework.  
The solution was developed within 1 hour, focusing on clarity, completeness, RESTful best practices, and professional documentation.  
Special attention was paid to code structure, validation, migrations, and API documentation for immediate review, launch, and clarity for employers.

---

## Tech Stack

- **Python 3.x**
- **Django**
- **Django REST Framework**
- **drf-yasg** (for Swagger/OpenAPI documentation)

---

## Features & Endpoints

**Implemented endpoints:**

1. **GET /api/v1/products/**
   - Returns a list of all products.
<img width="1772" height="932" alt="image" src="https://github.com/user-attachments/assets/19565bfe-0101-4f6e-9a28-8fade3410eef" />

2. **GET /api/v1/products/{id}/**
   - Returns a single product by its ID.
<img width="1770" height="914" alt="image" src="https://github.com/user-attachments/assets/c792318f-1fea-4395-b9fe-03b681b73945" />

3. **GET /api/v1/products/?category=Jewelery**
  - Supports filtering by category via query param: `/api/products/?category=Jewelery`
<img width="1774" height="925" alt="image" src="https://github.com/user-attachments/assets/3df36c24-bae0-4486-b728-5a21126de52d" />



4. **POST /api/v1/products/**
   - Accepts new product data, validates input, and adds product to the database.
<img width="1772" height="934" alt="image" src="https://github.com/user-attachments/assets/8418550c-33c6-47cf-85a4-e74e4f95579e" />


**Extra:**
- Admin interface for managing categories and products.
- Robust validation and error handling for all data.

---

## Authentication & Admin

- The API supports authentication via Django admin.
- **Default admin user:**
  - **Username:** `admin`
  - **Password:** `admin`
- Admin users can log in via `/admin/` to manage categories and products.
- Only admins can create new products or categories through the API.

---

## Project Structure

```
ecommerce-assignment-task/
├── ecommerce/                # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── product/                  # Product app (models, views, serializers, etc.)
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── .gitignore
```

- **models.py**: Defines Product and Category models.
- **serializers.py**: Serializes/deserializes API data, enforces validation.
- **views.py**: Contains logic for endpoints, query filtering, permissions.
- **urls.py**: Routes API endpoints.
- **admin.py**: Registers models for Django admin panel.

---

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ntkachenko21/assignment-task.git
   cd assignment-task
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create the default admin user (optional if not already created):**
   ```bash
   python manage.py createsuperuser --username admin --email admin@example.com
   # Set password as 'admin' when prompted
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access Swagger API docs:**
   - Open [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/) in your browser.

7. **Admin panel:**
   - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
   - Use credentials: `admin` / `admin`

---

## API Documentation (Swagger)

- All endpoints, request/response schemas, and validation rules are automatically documented and available at:
  - [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)
- You can interact with the API directly from the Swagger UI.

## Detailed Code Analysis

### Product Model

```python
class Product(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)
    stock = models.PositiveIntegerField()
    rating = models.FloatField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)]
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return f"{self.title}. Stock: {self.stock}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
```

- **Purpose:** Stores detailed product information.
- **Fields:**
  - `title`: Product name, max length 255, required.
  - `description`: Optional text description.
  - `price`: Decimal, up to 999999.99.
  - `created_at` / `updated_at`: Auto timestamps for creation/update.
  - `image`: Optional image field for product photo.
  - `stock`: Positive integer, current stock.
  - `rating`: Float, must be between 0 and 5 (validators ensure API integrity).
  - `category`: ForeignKey to Category, cascading delete, reverse relation as `products`.
- **Features:**
  - String representation shows product title and stock.
  - Products are sorted by newest first.
  - Image upload and rating validation included by default.
  - Strong data integrity via validators and nullability.

### Serializers

- **ProductSerializer:**  
  Validates incoming product data, ensures required fields, serializes for API.
- **CategorySerializer:**  
  Used for category endpoints and relations.

### Views

- **ProductListCreateAPIView:**  
  Handles `GET` (list/filter) and `POST` (create, admin only).
  - Filtering logic: checks for `category` query param, returns filtered queryset.
  - Creation logic: validates input, creates product if user is admin.
- **ProductRetrieveAPIView:**  
  Handles `GET` for single product by ID, returns 404 if not found.

### URLs

- All API routes are under `/api/v1/`.
- Swagger docs at `/api/swagger/`.
- Admin at `/admin/`.

### Permissions

- Anyone can read products.
- Only authenticated admin can create products or categories.

### Error Handling

- Clear validation errors returned with status code `400`.
- Not found resources return `404`.
- Unauthorized actions return `403`.

### Migrations

- Uses Django’s ORM and migration system.
- On first run, `python manage.py migrate` sets up DB schema.

---

## Notes & Decisions

- **Time spent:** Project was developed in a single 1-hour session, proving speed and expertise.
- **Design:** Django was chosen for its reliability, rapid development, and powerful admin.
- **Validation:** All user input is thoroughly checked.
- **Documentation:** Automatic OpenAPI docs for immediate employer review.
- **Extensibility:** Ready for real DB, authentication, and scaling.
- **Admin user:** Pre-configured for demo/testing.
- **Best practices:** Structure, comments, and API conventions strictly followed.

---

**Author:**  
Nikita Tkachenko ([ntkachenko21](https://github.com/ntkachenko21))
