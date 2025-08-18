from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_tables
from app.api.event_router import router as event_router
from app.api.menu_router import router as menu_router
from app.api.vote_router import router as vote_router

app = FastAPI(
    title="Event Management API",
    description="API for managing dining events, menus, and voting",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriate origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(event_router)
app.include_router(menu_router)
app.include_router(vote_router)


@app.on_event("startup")
def startup_event():
    """Create database tables on startup"""
    create_tables()


@app.get("/")
def read_root():
    return {"message": "Welcome to Event Management API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 