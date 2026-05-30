import os
import logging
from typing import Optional
from supabase import create_client, Client

# Configure logging
logger = logging.getLogger("supabase_client")
logging.basicConfig(level=logging.INFO)

# Load variables
SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")

# Initialize client placeholder
supabase: Optional[Client] = None

# Helper to check if credentials are valid and not defaults
def is_valid_config() -> bool:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False
    if "your-project-id" in SUPABASE_URL or "your_supabase_project_url" in SUPABASE_URL:
        return False
    if "your-supabase-anon-public-key" in SUPABASE_KEY or "your_supabase_anon_public_key" in SUPABASE_KEY:
        return False
    return True

# Initialize client
if is_valid_config():
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Successfully initialized Supabase Client.")
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {str(e)}")
        supabase = None
else:
    logger.warning("Supabase environment variables are missing or set to default placeholders. Running in Local Fallback Mode.")
    supabase = None

def get_supabase_client() -> Optional[Client]:
    """
    Returns the initialized Supabase client if configured, else None.
    """
    return supabase
