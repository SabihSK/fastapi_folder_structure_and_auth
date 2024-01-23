"""Config file of app."""
import os

from dotenv import load_dotenv

load_dotenv()

dbConnectionUrl = os.getenv("DATABASE_URL")
dbAsyncConnectionUrl = os.getenv("ASYNC_DATABASE_URL")
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_EMAIL_PASS")
origins = [
    os.getenv("FRONTEND_ORIGIN_1"),
    os.getenv("FRONTEND_ORIGIN_2"),
]
