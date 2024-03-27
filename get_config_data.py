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
    try:
        from config import Mail_Config

        return Mail_Config
    except:
        assert False, """
config.py 파일을 README.MD 를 참고하여 수정해 주세요.
그전에 호연님께 허락을 맡으시고 config.py 파일을 받아 오셔도 됩니다.
"""
