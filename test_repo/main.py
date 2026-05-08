
import logging
from auth import validate_token

# Configure logging
logging.basicConfig(level=logging.INFO)

def login(token):
    logging.info(f"Login attempt with token: {token}")

    if validate_token(token):
        logging.info("Token is valid. Login successful.")
        return True

    logging.warning("Token is invalid. Login failed.")
    return False