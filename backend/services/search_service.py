"""
Search service using Google Maps Places API for REAL local businesses.
"""
import httpx
import logging
from typing import List, Dict, Any
import googlemaps
from config.settings import settings

logger = logging.getLogger(__name__)


class SearchService:
    """Service for searching ACTUAL local businesses using Google Maps."""
    
    def __init__(self):
        self.serper_key = settings.serper_api_key
        self.serper_url = "https://google.serper.dev/search"
        
        # Try to initialize Google Maps
        self.gmaps = None
        self.use_maps = False
        
        if settings.google_maps_api_key:
            try:
                self.gmaps = googlemaps.Client(key=settings.google_maps_api_key)
                self.use_maps = True
                logger.info("✅ Google Maps API initialized - will get REAL business names!")
            except Exception as e:
                logger.warning(f"Google Maps init failed: {e}")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for ACTUAL local businesses (not listing pages).
        
        Args:
            query: Search query (e.g., "gyms in bageshwar")
            max_results: Number of REAL businesses to return
            
        Returns:
            List of ACTUAL business results with real names
        """
        # Use Google Maps if available
        if self.use_maps and self.gmaps:
            try:
                logger.info(f"Using Google Maps to find REAL businesses for: {query}")
                results = await self._search_google_maps(query, max_results)
                if results and len(results) > 0:
                    logger.info(f"✅ Found {len(results)} REAL businesses from Google Maps")
                    return results
                else:
                    logger.warning("Google Maps returned 0 results, trying Serper...")
            except Exception as e:
                logger.error(f"Google Maps error: {e}")
        
        # Fallback to Serper
        logger.warning("⚠️ Using Serper fallback - results may include listing pages")
        return await self._search_serper(query, max_results)
    
    async def _search_google_maps(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Google Maps Places API for REAL businesses."""
        results = []
        
        try:
            # Text Search
            logger.info(f"Searching Google Maps for: {query}")
            places_result = self.gmaps.places(query=query)
            
            if not places_result.get('results'):
                logger.warning(f"No places found for: {query}")
                return []
            
            logger.info(f"Google Maps returned {len(places_result['results'])} places")
            
            # Get details for each place
            for idx, place in enumerate(places_result['results'][:max_results * 2]):
                try:
                    place_id = place.get('place_id')
                    name = place.get('name', '')
                    
                    # Skip listing pages
                    if self._is_listing_page(name):
                        logger.info(f"Skipping listing page: {name}")
                        continue
                    
                    # Get detailed information (REMOVED 'types' from fields)
                    details_result = self.gmaps.place(
                        place_id=place_id,
                        fields=['name', 'formatted_address', 'formatted_phone_number',
                               'website', 'rating', 'opening_hours', 'url']  # ← FIXED: removed 'types'
                    )
                    
                    details = details_result.get('result', {})
                    
                    # Build result
                    website = details.get('website', '')
                    has_website = bool(website and website.strip())
                    
                    result = {
                        "title": details.get('name', name),
                        "link": website if has_website else "",
                        "snippet": details.get('formatted_address', ''),
                        "rating": str(details.get('rating', '')) if details.get('rating') else '',
                        "phone": details.get('formatted_phone_number', ''),
                        "address": details.get('formatted_address', ''),
                        "hours": self._format_hours(details.get('opening_hours')),
                        "is_place": True,
                        "google_maps_url": details.get('url', '')
                    }
                    
                    results.append(result)
                    logger.info(f"✅ Added: {result['title']} (Website: {'Yes' if has_website else 'NO - PRIORITY'})")
                    
                    if len(results) >= max_results:
                        break
                        
                except Exception as e:
                    logger.error(f"Error getting place details: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Google Maps search failed: {e}")
            return []
    
    def _is_listing_page(self, name: str) -> bool:
        """Check if name looks like a listing page."""
        name_lower = name.lower()
        
        # Patterns that indicate listing pages
        listing_patterns = [
            'best', 'top', 'list of', 'gyms in', 'cafes in', 
            'restaurants in', 'fitness centers', 'fitness centres',
            'near me', 'directory', 'available on', 'one of the best'
        ]
        
        return any(pattern in name_lower for pattern in listing_patterns)
    
    def _format_hours(self, hours_data) -> str:
        """Format opening hours from Google Maps."""
        if not hours_data:
            return ""
        
        weekday_text = hours_data.get('weekday_text', [])
        if weekday_text and len(weekday_text) > 0:
            return weekday_text[0]
        
        return ""
    
    async def _search_serper(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Fallback: Serper search."""
        headers = {
            "X-API-KEY": self.serper_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": 50
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.serper_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                results = []
                
                # Get local places
                places = data.get("places", [])
                for place in places:
                    if len(results) >= max_results:
                        break
                    
                    name = place.get("title", "")
                    if self._is_listing_page(name):
                        continue
                    
                    results.append({
                        "title": name,
                        "link": place.get("website", ""),
                        "snippet": place.get("address", ""),
                        "rating": str(place.get("rating", "")) if place.get("rating") else "",
                        "phone": place.get("phoneNumber", ""),
                        "address": place.get("address", ""),
                        "hours": place.get("hours", ""),
                        "is_place": True
                    })
                
                # Add organic results
                if len(results) < max_results:
                    organic = data.get("organic", [])
                    
                    exclude_domains = [
                        "instagram.com", "facebook.com", "twitter.com",
                        "youtube.com", "reddit.com", "quora.com"
                    ]
                    
                    for result in organic:
                        if len(results) >= max_results:
                            break
                        
                        title = result.get("title", "")
                        link = result.get("link", "").lower()
                        
                        if self._is_listing_page(title):
                            continue
                        
                        if any(d in link for d in exclude_domains):
                            continue
                        
                        results.append({
                            "title": title,
                            "link": result.get("link", ""),
                            "snippet": result.get("snippet", ""),
                            "rating": "",
                            "phone": "",
                            "address": "",
                            "hours": "",
                            "is_place": False
                        })
                
                return results[:max_results]
                
        except Exception as e:
            logger.error(f"Serper error: {e}")
            raise


# Singleton instance
search_service = SearchService()