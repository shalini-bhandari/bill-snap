from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.rate_limiter import limiter
from app.routes.bills import router as bills_router
from app.config import settings

app = FastAPI(
    title="Bill Snap API",
    description="An AI-powered bill scanning and expense management API",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

allowed_origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bills_router)

@app.get("/")
def root() :
    return {
        "message": "Welcome to Bill Snap API"
    }

@app.get("/api/health")
def health_check() :
    return {
        "status": "healthy"
    }