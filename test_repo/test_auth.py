
import logging
from auth import validate_token

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def test_valid_token():
    logging.info("Testing valid token")
    assert validate_token("valid")

def test_invalid_token():
    logging.info("Testing invalid token")
    assert not validate_token("bad")