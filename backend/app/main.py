from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.admin.auth import authentication_backend
from app.admin.views import (
    CategoryAdmin,
    SubscriberAdmin,
    UserAdmin,
    VenueAdmin,
    VenuePhotoAdmin,
    VenueStagingAdmin,
    VibeTagAdmin,
)
from app.api.v1.endpoints.subscribers import router as subscribers_router
from app.api.v1.endpoints.venues import router as venues_router
from app.core.config import settings
from app.core.database import engine
from app.core.users import auth_backend, fastapi_users_instance
from app.schemas.user import UserCreate, UserRead, UserUpdate

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Trust proxy headers for HTTPS reverse proxies
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register FastAPI-Users Auth & User Routers
app.include_router(
    fastapi_users_instance.get_auth_router(auth_backend),
    prefix=f"{settings.API_V1_STR}/auth/cookie",
    tags=["Auth"],
)
app.include_router(
    fastapi_users_instance.get_register_router(UserRead, UserCreate),
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users_instance.get_users_router(UserRead, UserUpdate),
    prefix=f"{settings.API_V1_STR}/users",
    tags=["Users"],
)

from app.api.v1.endpoints.admin_scrape import router as admin_scrape_router
from app.api.v1.endpoints.subscribers import router as subscribers_router
from app.api.v1.endpoints.venues import router as venues_router

# Register API v1 Business Routers
app.include_router(venues_router, prefix=settings.API_V1_STR, tags=["Venues"])
app.include_router(subscribers_router, prefix=settings.API_V1_STR, tags=["Subscribers"])
app.include_router(admin_scrape_router, prefix=settings.API_V1_STR, tags=["Admin"])


from app.admin.views import (
    CategoryAdmin,
    ScraperAdminView,
    SubscriberAdmin,
    UserAdmin,
    VenueAdmin,
    VenuePhotoAdmin,
    VenueStagingAdmin,
    VibeTagAdmin,
)

# Initialize SQLAdmin Dashboard
admin = Admin(app, engine, title="Bar in Cairo Admin", authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(VenueAdmin)
admin.add_view(VenueStagingAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(VibeTagAdmin)
admin.add_view(VenuePhotoAdmin)
admin.add_view(SubscriberAdmin)
admin.add_view(ScraperAdminView)



@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "version": settings.VERSION}
