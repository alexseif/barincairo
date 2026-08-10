from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.api.v1.endpoints.subscribers import router as subscribers_router
from app.api.v1.endpoints.venues import router as venues_router
from app.admin.views import CategoryAdmin, SubscriberAdmin, VenueAdmin, VenuePhotoAdmin, VibeTagAdmin
from app.core.config import settings
from app.core.database import engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
app.include_router(venues_router, prefix=settings.API_V1_STR, tags=["Venues"])
app.include_router(subscribers_router, prefix=settings.API_V1_STR, tags=["Subscribers"])

# Initialize SQLAdmin Dashboard
admin = Admin(app, engine, title="Bar in Cairo Admin")
admin.add_view(VenueAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(VibeTagAdmin)
admin.add_view(VenuePhotoAdmin)
admin.add_view(SubscriberAdmin)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "version": settings.VERSION}
