# pyright: reportGeneralTypeIssues=false
from os import environ
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bot:
    token: str

@dataclass
class Database:
    username: str
    password: str
    host: str
    port: int
    db_name: str

@dataclass
class Bill:
    username: str
    password: str
    expiration_date: str
    url: str
    redirect_url: str

@dataclass
class Spreadsheets:
    type_: str 
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: int
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str

@dataclass
class Logger:
    path: str
    level: str

@dataclass
class Config:
    bot: Bot
    database: Database
    bill: Bill
    spreadsheets: Spreadsheets
    logger: Logger


def load_config():
    load_dotenv()

    return Config(
        bot = Bot(
            token = environ.get("BOT_TOKEN", ""),
        ),
        database = Database(
            username = environ.get("POSTGRES_USERNAME"),
            password = environ.get("POSTGRES_PASSWORD"),
            host = environ.get("POSTGRES_HOST"),
            port = environ.get("POSTGRES_PORT"),
            db_name = environ.get("POSTGRES_DB_NAME"),
        ),
        bill = Bill(
            username = environ.get("BILL_USERNAME"),
            password = environ.get("BILL_PASSWORD"),
            expiration_date = environ.get("BILL_EXPIRATION_DATE"),
            url = environ.get("BILL_URL"),
            redirect_url = environ.get("BILL_REDIRECT_URL"),
        ),
        spreadsheets = Spreadsheets(
            type_ = environ.get("SPREADSHEETS_TYPE"),
            project_id = environ.get("SPREADSHEETS_PROJECT_ID"),
            private_key_id = environ.get("SPREADSHEETS_PRIVATE_KEY_ID"),
            private_key = environ.get("SPREADSHEETS_PRIVATE_KEY"),
            client_email = environ.get("SPREADSHEETS_CLIENT_EMAIL"),
            client_id = environ.get("SPREADSHEETS_CLIENT_ID"),
            auth_uri = environ.get("SPREADSHEETS_AUTH_URI"),
            token_uri = environ.get("SPREADSHEETS_TOKEN_URI"),
            auth_provider_x509_cert_url = environ.get("SPREADSHEETS_AUTH_PROVIDER_X509_CERT_URL"),
            client_x509_cert_url = environ.get("SPREADSHEETS_CLIENT_X509_CERT_URL"),
        ),
        logger = Logger(
            path = environ.get("LOGGER_PATH"),
            level = "DEBUG",
        ),
    )
