# Architectural Specification: Admin Area Architecture

**Feature Goal**: Document the FastAPI + SQLAdmin management dashboard, zero-trust session authentication, environment credential guards (`SEC-1.4`), and model administration views for venues, categories, vibe tags, photos, and subscribers.  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Implemented  

---

## 1. Architectural Scope, Isolation & Design Patterns

### 1.1 Scope Boundaries & Isolation
- **In-Scope Target Modules**:
  - `backend/app/admin/auth.py`
  - `backend/app/admin/views.py`
  - `backend/app/main.py`
  - `backend/app/core/config.py`
- **Out-of-Scope / Non-Goals**:
  - Public end-user registration or public JWT auth (admin access is strictly restricted to session-based administrative users).

### 1.2 Layered Architecture & Separation of Concerns
- **Authentication Layer (`backend/app/admin/auth.py`)**: `AdminAuth` class extending SQLAdmin `AuthenticationBackend`, handling login credentials, session management, and logout.
- **View Presentation Layer (`backend/app/admin/views.py`)**: ModelAdmin classes defining column lists, search fields, filters, and form inputs for database entities.
- **Database Engine Binding (`backend/app/main.py`)**: SQLAdmin instance mounted directly at `/admin` bound to the SQLAlchemy async engine.

---

## 2. Admin Views & Data Model Specifications

### 2.1 Admin View Registry
The following views are mounted and active at `/admin`:

| View Class | Target Model | Display Columns | Search Fields | Features |
| :--- | :--- | :--- | :--- | :--- |
| `VenueAdmin` | `Venue` | `id`, `name_en`, `name_ar`, `price_range`, `is_active` | `name_en`, `name_ar`, `slug` | Latitude/Longitude geometry input helpers |
| `CategoryAdmin` | `Category` | `id`, `name_en`, `name_ar`, `slug` | `name_en`, `name_ar` | Venue taxonomy management |
| `VibeTagAdmin` | `VibeTag` | `id`, `name_en`, `name_ar`, `slug` | `name_en`, `slug` | Atmosphere filter tags |
| `VenuePhotoAdmin` | `VenuePhoto` | `id`, `venue_id`, `photo_url`, `is_primary` | `photo_url` | Media reference management |
| `SubscriberAdmin` | `Subscriber` | `id`, `whatsapp_number`, `created_at` | `whatsapp_number` | WhatsApp dispatch roster |

### 2.2 Security Implementation (`auth.py`)
```python
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"token": "authenticated"})
            return True
        return False

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == "authenticated"
```

---

## 3. Zero-Trust Security Compliance Checklist

- [x] **SEC-1.1**: Form payload fields parsed and validated securely by Starlette request forms.
- [x] **SEC-1.2**: Admin database queries executed via parameterized SQLAlchemy async ORM sessions.
- [x] **SEC-1.3**: Output strings in view columns sanitized against XSS attacks.
- [x] **SEC-1.4**: Admin credentials loaded dynamically from `.env` via `settings.ADMIN_USERNAME` and `settings.ADMIN_PASSWORD` with defensive fallback warnings so missing variables do not break container builds.
- [x] **SEC-1.5**: Admin session cookies configured with HTTP-only flags and isolated routing paths.

---

## 4. Verification & Developer Instructions

- **Access URL**: `http://127.0.0.1:8000/admin`
- **Login Verification**: Authenticate using configured `ADMIN_USERNAME` and `ADMIN_PASSWORD`.
