from mysql_config import mysql_db

def get_mysql_url() -> str:
    return f"mysql://{mysql_db['user']}:{mysql_db['password']}@{mysql_db['host']}:{mysql_db['port']}/{mysql_db['database']}?charset={mysql_db['charset']}"


def get_mysql_dict() -> dict:
    return mysql_db


SERVICE_DB_PADDING = "log_"


def set_db_padding(padding: str = "log_"):
    global SERVICE_DB_PADDING
    SERVICE_DB_PADDING = padding


def get_db_padding() -> str:
    return SERVICE_DB_PADDING


def get_mail_object():
    from config import Mail_Config

    return Mail_Config
