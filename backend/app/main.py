from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from app.core.config import settings
from app.routes.api import api_router
from app.core.database import create_tables, wait_for_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    
    # Wait for DB to be ready
    wait_for_db()
    
    # Create tables
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}