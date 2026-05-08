import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def validate_token(token):
    logging.info(f"Validating token: {token}")
    return token == "valid"