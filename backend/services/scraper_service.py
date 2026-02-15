"""
Web scraper service to extract content from websites.
"""
import httpx
import logging
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for scraping website content."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    async def scrape_website(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a website and extract HTML content.
        
        Args:
            url: Website URL to scrape
            
        Returns:
            Dictionary with url, html_content, and success status
        """
        # Handle empty or invalid URLs
        if not url or url == "" or url == "N/A":
            return {
                "url": "",
                "html_content": "",
                "success": False,
                "error": "No website available"
            }
        
        try:
            async with httpx.AsyncClient(
                timeout=15.0,
                follow_redirects=True,
                headers=self.headers
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                html_content = response.text
                
                logger.info(f"Successfully scraped: {url}")
                return {
                    "url": url,
                    "html_content": html_content,
                    "success": True,
                    "status_code": response.status_code
                }
                
        except httpx.HTTPError as e:
            logger.warning(f"HTTP error scraping {url}: {e}")
            return {
                "url": url,
                "html_content": "",
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            logger.warning(f"Error scraping {url}: {e}")
            return {
                "url": url,
                "html_content": "",
                "success": False,
                "error": str(e)
            }
    
    async def scrape_multiple(self, urls: list) -> list:
        """
        Scrape multiple websites concurrently.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of scraping results
        """
        tasks = [self.scrape_website(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Exception during scraping: {result}")
                processed_results.append({
                    "url": "",
                    "html_content": "",
                    "success": False,
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def parse_html(self, html_content: str) -> BeautifulSoup:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html_content: Raw HTML string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html_content, 'lxml')


# Singleton instance
scraper_service = ScraperService()
