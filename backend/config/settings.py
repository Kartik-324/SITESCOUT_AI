"""
Configuration settings for the application.
Loads environment variables and provides centralized access to configuration.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openai_api_key: str
    serper_api_key: str
    google_maps_api_key: str = ""  

    # Google Sheets Configuration
    google_sheets_credentials_file: str = "credentials.json"
    google_sheet_id: str

    # SMTP Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None   # ← IMPORTANT
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None
    smtp_from_name: str = "SiteScout AI"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"   # 🔥 prevents extra field error


# Global settings instance
settings = Settings()
