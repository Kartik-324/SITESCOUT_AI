"""
Main FastAPI application for Lead Generation & Cold Email Automation System.
"""
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio

from config import settings
from services import (
    search_service,
    scraper_service,
    extractor_service,
    email_generator,
    sheets_service,
    mail_service
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Lead Generation & Cold Email Automation",
    description="AI-powered system for finding leads and generating cold emails",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class LeadGenerationRequest(BaseModel):
    """Request model for lead generation."""
    query: str = Field(..., description="Search query (e.g., 'best cafes in bhopal')")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of results")


class LeadData(BaseModel):
    """Model for a single lead."""
    business_name: str
    email: str
    phone: str
    rating: str
    website: str
    address: str
    website_exists: bool
    cold_email: str


class LeadGenerationResponse(BaseModel):
    """Response model for lead generation."""
    success: bool
    message: str
    total_leads: int
    leads: List[LeadData]
    saved_to_sheets: bool


class SendEmailRequest(BaseModel):
    """Request model for sending emails."""
    leads: List[Dict[str, Any]]
    subject: str = "Business Opportunity"


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Lead Generation & Cold Email Automation",
        "version": "1.0.0"
    }


@app.post("/generate-leads", response_model=LeadGenerationResponse)
async def generate_leads(request: LeadGenerationRequest):
    """
    Main endpoint to generate leads from a search query.
    
    Process:
    1. Search Google using Serper API
    2. Scrape websites (or skip if no website)
    3. Extract business data using OpenAI
    4. Generate cold emails
    5. Save to Google Sheets
    """
    try:
        logger.info(f"Starting lead generation for query: {request.query}")
        
        # Step 1: Search Google
        logger.info("Step 1: Searching Google...")
        search_results = await search_service.search(
            query=request.query,
            max_results=request.max_results
        )
        
        if not search_results:
            raise HTTPException(
                status_code=404,
                detail="No search results found"
            )
        
        logger.info(f"Found {len(search_results)} search results")
        
        # Step 2 & 3: Process each result
        leads = []
        
        for idx, search_result in enumerate(search_results):
            if len(leads) >= request.max_results:
                break
            
            url = search_result.get("link", "")
            search_title = search_result.get("title", "")
            
            logger.info(f"Processing result {idx + 1}: {search_title}")
            
            # Check if business has website
            if not url or url == "":
                # Business without website
                logger.info(f"Business without website: {search_title}")
                business_data = await extractor_service.extract_business_data(
                    html_content="",
                    url="",
                    search_title=search_title,
                    search_data=search_result
                )
            else:
                # Business with website - try to scrape
                scrape_result = await scraper_service.scrape_website(url)
                
                if scrape_result.get("success"):
                    business_data = await extractor_service.extract_business_data(
                        html_content=scrape_result["html_content"],
                        url=url,
                        search_title=search_title,
                        search_data=search_result
                    )
                else:
                    # Failed to scrape - use search data
                    logger.warning(f"Failed to scrape {url}, using search data only")
                    business_data = await extractor_service.extract_business_data(
                        html_content="",
                        url=url,
                        search_title=search_title,
                        search_data=search_result
                    )
            
            # Step 4: Generate cold email
            logger.info(f"Generating cold email for {business_data['business_name']}")
            cold_email = await email_generator.generate_cold_email(business_data)
            business_data["cold_email"] = cold_email
            
            leads.append(business_data)
            logger.info(f"Added lead {len(leads)}/{request.max_results}: {business_data['business_name']}")
        
        if not leads:
            raise HTTPException(
                status_code=404,
                detail="No valid leads could be extracted"
            )
        
        logger.info(f"Successfully processed {len(leads)} leads")
        
        # Step 5: Save to Google Sheets
        logger.info("Step 5: Saving to Google Sheets...")
        saved_to_sheets = sheets_service.append_leads(leads)
        
        return LeadGenerationResponse(
            success=True,
            message=f"Successfully generated {len(leads)} leads",
            total_leads=len(leads),
            leads=[LeadData(**lead) for lead in leads],
            saved_to_sheets=saved_to_sheets
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating leads: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/send-emails")
async def send_emails(request: SendEmailRequest):
    """Send cold emails to leads."""
    try:
        logger.info(f"Sending emails to {len(request.leads)} recipients")
        
        recipients = []
        for lead in request.leads:
            if lead.get("email") and lead.get("cold_email"):
                recipients.append({
                    "email": lead["email"],
                    "body": lead["cold_email"]
                })
        
        if not recipients:
            raise HTTPException(
                status_code=400,
                detail="No valid recipients found"
            )
        
        results = await mail_service.send_bulk_emails(
            recipients=recipients,
            subject_template=request.subject
        )
        
        return {
            "success": True,
            "sent": results["sent"],
            "failed": results["failed"],
            "errors": results["errors"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending emails: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "api": "online",
            "openai": "configured" if settings.openai_api_key else "not configured",
            "serper": "configured" if settings.serper_api_key else "not configured",
            "google_sheets": "configured" if settings.google_sheet_id else "not configured",
            "smtp": "configured" if settings.smtp_username else "not configured"
        }
    }


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )