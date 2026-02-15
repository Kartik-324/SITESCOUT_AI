"""
Data extraction service using OpenAI to structure scraped data.
"""
import re
import json
import logging
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from config.settings import settings

logger = logging.getLogger(__name__)


class ExtractorService:
    """Service for extracting structured data from HTML using OpenAI."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o-mini"
    
    def extract_emails_regex(self, text: str) -> list:
        """
        Extract email addresses using regex.
        
        Args:
            text: Text to search for emails
            
        Returns:
            List of found email addresses
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Filter out common false positives
        filtered_emails = [
            email for email in emails 
            if not any(x in email.lower() for x in ['example.com', 'test.com', 'placeholder'])
        ]
        
        return list(set(filtered_emails))  # Remove duplicates
    
    async def extract_business_data(
        self, 
        html_content: str, 
        url: str,
        search_title: str = "",
        search_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Extract structured business data from HTML using OpenAI or search metadata.
        
        Args:
            html_content: Raw HTML content
            url: Website URL
            search_title: Original search result title
            search_data: Additional data from search (rating, phone, address, etc.)
            
        Returns:
            Dictionary with extracted business information
        """
        # Initialize with search data if available
        if search_data is None:
            search_data = {}
        
        # If no website, use only search data
        if not url or url == "" or not html_content:
            emails = []
            data = {
                "business_name": search_data.get("title", search_title),
                "owner_name": "",
                "rating": search_data.get("rating", ""),
                "opening_hours": search_data.get("hours", ""),
                "phone": search_data.get("phone", ""),
                "address": search_data.get("address", search_data.get("snippet", "")),
                "email": "",
                "website": "N/A",
                "website_exists": False
            }
            logger.info(f"Business without website: {data['business_name']}")
            return data
        
        # Extract emails using regex
        emails = self.extract_emails_regex(html_content)
        
        # Truncate HTML to avoid token limits
        truncated_html = html_content[:8000]
        
        prompt = f"""
Extract business information from the following HTML content.

Website URL: {url}
Search Title: {search_title}

Return ONLY a valid JSON object with these exact fields:
{{
    "business_name": "extracted business name or from title",
    "owner_name": "owner/founder name if found, otherwise empty string",
    "rating": "rating if found (e.g., 4.5), otherwise empty string",
    "opening_hours": "opening hours if found, otherwise empty string",
    "phone": "phone number if found, otherwise empty string",
    "address": "address if found, otherwise empty string"
}}

HTML Content:
{truncated_html[:4000]}

Return ONLY the JSON object, no other text.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data extraction expert. Extract business information and return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            # Parse JSON
            data = json.loads(content)
            
            # Merge with search data (prefer extracted data)
            data["email"] = emails[0] if emails else ""
            data["website"] = url
            data["website_exists"] = True
            
            # Fill missing fields from search data
            if not data.get("rating") and search_data.get("rating"):
                data["rating"] = search_data.get("rating")
            if not data.get("phone") and search_data.get("phone"):
                data["phone"] = search_data.get("phone")
            if not data.get("address") and search_data.get("address"):
                data["address"] = search_data.get("address")
            if not data.get("opening_hours") and search_data.get("hours"):
                data["opening_hours"] = search_data.get("hours")
            
            logger.info(f"Successfully extracted data from {url}")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {url}: {e}")
            return self._get_default_data(url, emails, search_title, search_data)
        except Exception as e:
            logger.error(f"Error extracting data from {url}: {e}")
            return self._get_default_data(url, emails, search_title, search_data)
    
    def _get_default_data(self, url: str, emails: list, title: str = "", search_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Return default data structure when extraction fails.
        
        Args:
            url: Website URL
            emails: List of found emails
            title: Search result title
            search_data: Additional search metadata
            
        Returns:
            Default data dictionary
        """
        if search_data is None:
            search_data = {}
        
        return {
            "business_name": search_data.get("title", title if title else url),
            "owner_name": "",
            "rating": search_data.get("rating", ""),
            "opening_hours": search_data.get("hours", ""),
            "phone": search_data.get("phone", ""),
            "address": search_data.get("address", search_data.get("snippet", "")),
            "email": emails[0] if emails else "",
            "website": url if url else "N/A",
            "website_exists": bool(url and url != "N/A")
        }


# Singleton instance
extractor_service = ExtractorService()