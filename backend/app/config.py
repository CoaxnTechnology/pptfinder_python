import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


class Settings:
    PROJECT_NAME: str = "PPT Finder API"
    PROJECT_VERSION: str = "1.0.0"

    # -----------------------------
    # PostgreSQL Database
    # -----------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("❌ DATABASE_URL is missing in the .env file")

    # -----------------------------
    # Google Custom Search API
    # -----------------------------
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID: str = os.getenv("SEARCH_ENGINE_ID")  # Updated ✔

    if not GOOGLE_API_KEY:
        raise ValueError("❌ GOOGLE_API_KEY is missing in the .env file")

    if not SEARCH_ENGINE_ID:
        raise ValueError("❌ SEARCH_ENGINE_ID is missing in the .env file")


settings = Settings()
