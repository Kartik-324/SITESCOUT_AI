"""
Google Sheets service for saving lead data.
"""
import logging
from typing import List, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.settings import settings

logger = logging.getLogger(__name__)


class SheetsService:
    """Service for managing Google Sheets operations."""
    
    def __init__(self):
        self.credentials_file = settings.google_sheets_credentials_file
        self.sheet_id = settings.google_sheet_id
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Sheets API service."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.scopes
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Google Sheets service: {e}")
            raise
    
    def _ensure_headers(self):
        """Ensure the sheet has proper headers."""
        headers = [
            "Business Name",
            "Email",
            "Phone",
            "Rating",
            "Website",
            "Address",
            "Website Exists",
            "Cold Email"
        ]
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='A1:H1'
            ).execute()
            
            values = result.get('values', [])
            
            if not values or values[0] != headers:
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.sheet_id,
                    range='A1:H1',
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
                logger.info("Headers created/updated in sheet")
                
        except HttpError as e:
            logger.error(f"Error ensuring headers: {e}")
            raise
    
    def append_leads(self, leads: List[Dict[str, Any]]) -> bool:
        """Append lead data to the Google Sheet."""
        try:
            self._ensure_headers()
            
            rows = []
            for lead in leads:
                row = [
                    lead.get("business_name", ""),
                    lead.get("email", ""),
                    lead.get("phone", ""),
                    lead.get("rating", ""),
                    lead.get("website", ""),
                    lead.get("address", ""),
                    str(lead.get("website_exists", True)),
                    lead.get("cold_email", "")
                ]
                rows.append(row)
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range='A:H',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': rows}
            ).execute()
            
            logger.info(f"Appended {len(rows)} leads to Google Sheet")
            return True
            
        except HttpError as e:
            logger.error(f"HTTP error appending to sheet: {e}")
            return False
        except Exception as e:
            logger.error(f"Error appending to sheet: {e}")
            return False
    
    def clear_sheet(self) -> bool:
        """Clear all data from the sheet (except headers)."""
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range='A2:H'
            ).execute()
            
            logger.info("Sheet cleared successfully")
            return True
            
        except HttpError as e:
            logger.error(f"Error clearing sheet: {e}")
            return False


# Singleton instance
sheets_service = SheetsService()