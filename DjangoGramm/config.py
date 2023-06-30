import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
EMAIL_ADDRESS = os.getenv('EMAIL_ADD')
