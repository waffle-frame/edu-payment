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
    folder_id: str
    account_file: str

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
            folder_id = environ.get("SPREADSHEETS_FOLDER_ID"),
            account_file = environ.get("SPREADSHEETS_ACCOUNT_FILE"),
        ),
        logger = Logger(
            path = environ.get("LOGGER_PATH"),
            level = "DEBUG",
        ),
    )
