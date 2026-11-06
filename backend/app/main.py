from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.bills import router as bills_router

app = FastAPI(
    title="Bill Snap API",
    description="An AI-powered bill scanning and expense management API",
    version="1.0.0"
)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
]

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