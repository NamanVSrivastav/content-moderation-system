from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from app.api.v1.endpoints import moderation, stats
from app.core.config import settings
from app.core.logging import setup_logging

app = FastAPI(title="Content Moderation System", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(settings.REDIS_URL)

# Include API endpoints
app.include_router(moderation.router, prefix="/api/v1/moderate", tags=["Moderation"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Stats"])

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}