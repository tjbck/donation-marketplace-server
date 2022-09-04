from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER_DIR = './uploads'

ENV = os.environ.get('ENV', 'dev')

# To obtain a secure secret key this run: openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRET_KEY', 'SECRET_KEY')
RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET', 'RECAPTCHA_SECRET')


DB_CRED = os.environ.get('DB_CRED', "root:root")
DB_URL = os.environ.get('DB_URL',  "localhost:27017")

# Test Env Setup
if "pytest" in sys.modules:
    ENV = 'test'
    DB_CRED = 'root:root'
    DB_URL = 'localhost:27018'


client = MongoClient(
    f'mongodb://{DB_CRED}@{DB_URL}/?authSource=admin'
)

db = client['marketplace']
