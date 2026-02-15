"""
Email sending service using SMTP (Gmail compatible).
"""

import logging
import ssl
import aiosmtplib
from email.message import EmailMessage
from typing import List, Dict
from config.settings import settings

logger = logging.getLogger(__name__)


class MailService:
    """Service for sending emails via SMTP."""

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.from_name = settings.smtp_from_name

    def is_configured(self) -> bool:
        """Check if SMTP is properly configured."""
        return all([
            self.smtp_host,
            self.smtp_port,
            self.smtp_username,
            self.smtp_password,
            self.from_email
        ])

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        is_html: bool = False
    ) -> bool:
        """Send a single email."""

        if not self.is_configured():
            logger.warning("SMTP not configured. Skipping email.")
            return False

        try:
            message = EmailMessage()
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            message["Subject"] = subject

            if is_html:
                message.add_alternative(body, subtype="html")
            else:
                message.set_content(body)

            context = ssl.create_default_context()

            # Port handling
            if self.smtp_port == 465:
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.smtp_username,
                    password=self.smtp_password,
                    use_tls=True,
                    tls_context=context,
                )
            else:
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    username=self.smtp_username,
                    password=self.smtp_password,
                    start_tls=True,
                    tls_context=context,
                )

            logger.info(f"✅ Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {str(e)}")
            return False

    async def send_bulk_emails(
        self,
        recipients: List[Dict],
        subject_template: str = "Business Opportunity",
    ) -> Dict:
        """Send multiple emails."""

        results = {
            "sent": 0,
            "failed": 0,
            "errors": []
        }

        for recipient in recipients:
            email = recipient.get("email")
            body = recipient.get("body", "")

            if not email:
                results["failed"] += 1
                continue

            success = await self.send_email(
                to_email=email,
                subject=subject_template,
                body=body,
                is_html=False
            )

            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(email)

        logger.info(
            f"Bulk email completed: {results['sent']} sent, {results['failed']} failed"
        )

        return results


# Singleton instance
mail_service = MailService()
