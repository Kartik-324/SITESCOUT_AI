import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.mail_service import mail_service

async def test_email():
    print("Testing SMTP configuration...")
    print(f"SMTP Host: {mail_service.smtp_host}")
    print(f"SMTP Port: {mail_service.smtp_port}")
    print(f"SMTP Username: {mail_service.smtp_username}")
    print(f"From Email: {mail_service.from_email}")
    print(f"Configured: {mail_service.is_configured()}")
    print()
    
    if not mail_service.is_configured():
        print("❌ SMTP is NOT configured!")
        print("Check your .env file!")
        return
    
    print("Sending test email...")
    result = await mail_service.send_email(
        to_email="kartikjoshi1817@gmail.com",
        subject="Test Email - SiteScout AI",
        body="This is a test email from SiteScout AI!\n\nIf you receive this, SMTP is working perfectly!"
    )
    
    if result:
        print("✅ SUCCESS! Check your inbox!")
    else:
        print("❌ FAILED! Check the logs above for errors.")

if __name__ == "__main__":
    asyncio.run(test_email())