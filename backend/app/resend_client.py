import os
import logging
from typing import Optional

import resend

# Configure logging
logger = logging.getLogger("resend_client")
logging.basicConfig(level=logging.INFO)

# Load Resend configuration from environment
RESEND_API_KEY: Optional[str] = os.getenv("RESEND_API_KEY")
CONTACT_TO_EMAIL: str = os.getenv("CONTACT_TO_EMAIL", "sahiltalape2701@gmail.com")
CONTACT_FROM_EMAIL: str = os.getenv("CONTACT_FROM_EMAIL", "onboarding@resend.dev")

# Initialize Resend
_resend_ready = False

if RESEND_API_KEY and "your_resend_api_key" not in RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    _resend_ready = True
    logger.info("Resend API key configured successfully.")
else:
    logger.warning(
        "RESEND_API_KEY is missing or set to placeholder. "
        "Email delivery is disabled — contact submissions will fall back to local JSON storage."
    )


def is_resend_configured() -> bool:
    """Returns True if Resend is ready to send emails."""
    return _resend_ready


def send_contact_email(name: str, email: str, message: str) -> Optional[dict]:
    """
    Sends a contact form submission as an email via Resend.

    Args:
        name: Sender's name from the contact form.
        email: Sender's email address.
        message: The message body.

    Returns:
        Resend API response dict on success, or None on failure.
    """
    if not _resend_ready:
        logger.warning("Resend is not configured. Skipping email delivery.")
        return None

    try:
        params = {
            "from": CONTACT_FROM_EMAIL,
            "to": [CONTACT_TO_EMAIL],
            "subject": f"Portfolio Contact: {name}",
            "html": (
                f"<h2>New Contact Form Submission</h2>"
                f"<p><strong>Name:</strong> {name}</p>"
                f"<p><strong>Email:</strong> <a href='mailto:{email}'>{email}</a></p>"
                f"<hr>"
                f"<p><strong>Message:</strong></p>"
                f"<p>{message}</p>"
                f"<hr>"
                f"<p style='color: #888; font-size: 12px;'>Sent from your Portfolio contact form</p>"
            ),
            "reply_to": email,
        }

        response = resend.Emails.send(params)
        logger.info(f"Email sent successfully via Resend. Response: {response}")
        return response

    except Exception as e:
        logger.error(f"Failed to send email via Resend: {str(e)}")
        return None
