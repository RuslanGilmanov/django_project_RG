import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
EMAIL_ADDRESS = os.getenv('EMAIL_ADD')
SECRET_KEY = os.getenv('S_KEY')

# Database settings
DATABASE_NAME = os.getenv('DB_NAME')
DATABASE_USER = os.getenv('DB_USER')
DATABASE_PASS = os.getenv('DB_PASS')
DATABASE_HOST = os.getenv('DB_HOST')
DATABASE_PORT = os.getenv('DB_PORT')

# AWS S3 bucket settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
