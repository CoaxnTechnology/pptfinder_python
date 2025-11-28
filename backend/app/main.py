from app.routes import check_keyword, save_data,privacy_policy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import category
#privacy_policy
from app.database import Base, engine

# Create database tables (no Alembic required for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PPT Finder API",
    description="Search, save, and manage PPT links using Google Custom Search + Database caching",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(category.router)
app.include_router(check_keyword.router)
#app.include_router(google_search1.router)
app.include_router(save_data.router)
#app.include_router(privacy_policy.router)
app.include_router(privacy_policy.router)


@app.get("/")
def root():
    return {"message": "PPT Finder API running successfully!"}
