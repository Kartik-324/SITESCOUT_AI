"""
Email generation service using OpenAI to create personalized cold emails.
"""
import logging
from typing import Dict, Any
from openai import AsyncOpenAI
from config.settings import settings

logger = logging.getLogger(__name__)


class EmailGenerator:
    """Service for generating personalized cold emails."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o-mini"
    
    async def generate_cold_email(self, business_data: Dict[str, Any]) -> str:
        """
        Generate a personalized cold email for a business.
        
        Args:
            business_data: Dictionary containing business information
            
        Returns:
            Generated cold email text
        """
        business_name = business_data.get("business_name", "your business")
        rating = business_data.get("rating", "")
        owner_name = business_data.get("owner_name", "")
        website = business_data.get("website", "")
        has_website = business_data.get("website_exists", True)
        phone = business_data.get("phone", "")
        
        # Different approach for businesses with vs without websites
        if not has_website or website == "N/A":
            # Business WITHOUT website - more urgent pitch
            prompt = f"""
Write a short, compelling cold email to a business that DOES NOT have a website yet.

Business Details:
- Business Name: {business_name}
- Owner: {owner_name if owner_name else "Not specified"}
- Rating: {rating if rating else "Not specified"}
- Phone: {phone if phone else "Not specified"}
- **Status: NO WEBSITE** (This is your opportunity!)

Requirements:
1. Keep it under 120 words
2. Start with a specific observation about their business
3. Mention that they DON'T have a website yet (this is the opportunity)
4. If they have a good rating, acknowledge it and explain how a website could help them get MORE customers
5. Offer a FREE website audit or consultation
6. Emphasize how much business they're losing without online presence
7. Be professional but urgent - they're missing out!
8. Include a clear call-to-action
9. Sign with [Your Name]

Make it personal, not salesy. Focus on THEIR lost revenue/opportunity.

Return ONLY the email body, no subject line.
"""
        else:
            # Business WITH website - improvement pitch
            prompt = f"""
Write a short, professional cold email offering website improvement services.

Business Details:
- Business Name: {business_name}
- Owner: {owner_name if owner_name else "Not specified"}
- Rating: {rating if rating else "Not specified"}
- Website: {website}

Requirements:
1. Keep it under 120 words
2. Be professional but friendly
3. Mention their business name
4. If rating exists, acknowledge their good reputation
5. Offer a FREE website audit or improvement suggestions
6. Mention specific modern web features (mobile optimization, faster loading, better SEO)
7. Include a clear call-to-action
8. Sign with [Your Name]

Make it helpful, not pushy.

Return ONLY the email body, no subject line.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional business development expert who writes personalized, value-driven cold emails that focus on the client's needs and lost opportunities."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=350
            )
            
            email_content = response.choices[0].message.content.strip()
            
            logger.info(f"Generated cold email for {business_name} ({'no website' if not has_website else 'has website'})")
            return email_content
            
        except Exception as e:
            logger.error(f"Error generating email for {business_name}: {e}")
            return self._get_default_email(business_name, rating, has_website)
    
    def _get_default_email(self, business_name: str, rating: str = "", has_website: bool = True) -> str:
        """
        Generate a simple default email when AI generation fails.
        
        Args:
            business_name: Name of the business
            rating: Business rating if available
            has_website: Whether business has a website
            
        Returns:
            Default email template
        """
        if not has_website:
            rating_text = f"With your {rating} rating, " if rating else ""
            return f"""Hi,

I came across {business_name} and noticed you don't have a website yet. {rating_text}you're clearly doing great, but I wanted to reach out because you're likely missing out on significant revenue from customers who search online.

In today's market, 81% of customers check businesses online before visiting. Without a website, they're choosing your competitors instead.

I'd love to offer you a free consultation on getting your business online. It's easier and more affordable than you might think, and I can show you exactly how much business you're currently losing.

Would you be open to a quick 10-minute call this week?

Best regards,
[Your Name]
"""
        else:
            rating_text = f"With your {rating} rating, " if rating else ""
            return f"""Hi,

I came across {business_name} and was impressed by your online presence. {rating_text}I believe there might be opportunities to enhance your digital visibility and attract more customers.

I specialize in helping businesses like yours improve their websites and online marketing. Would you be open to a quick 15-minute call to discuss how we could help you grow?

Looking forward to hearing from you.

Best regards,
[Your Name]
"""


# Singleton instance
email_generator = EmailGenerator()
