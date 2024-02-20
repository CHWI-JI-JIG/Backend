import __init__
import pymysql

from icecream import ic


class MySqlMigrations:
    def __init__(self, name_padding: str = "log_"):
        self.name_padding = name_padding

    def connect(self):
        from get_config_data import get_mysql_dict

        sql_config = get_mysql_dict()
        return pymysql.connect(
            host=sql_config["host"],
            user=sql_config["user"],
            password=sql_config["password"],
            db=sql_config["database"],
            charset=sql_config["charset"],
        )

    def get_padding_name(self, name: str) -> str:
        return f"{self.name_padding}{name}"

    def create_user(self):
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        auth_table_name = self.get_padding_name("user_auth")

        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 생성 쿼리
                create_user_table_query = f"""
CREATE TABLE IF NOT EXISTS {user_table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pw VARCHAR(511) NOT NULL,
    account VARCHAR(50) UNIQUE,
    name VARCHAR(100) NOT NULL,
    nickname VARCHAR(50),
    time_of_try_login TIMESTAMP,
    lock_flag BOOLEAN,
    count_of_login_fail INT,
    post_last_update_date TIMESTAMP,
    post_num INT,
    delete_flag BOOLEAN
);
                """
                # user 생성
                cursor.execute(create_user_table_query)
                policy = ", ".join(
                    list(map(lambda x: f"'{x}'", Policy.__members__.keys()))
                )
                scope = ", ".join(
                    list(map(lambda x: f"'{x}'", TargetScope.__members__.keys()))
                )
                # UserAuth 테이블 생성 쿼리
                create_auth_table_query = f"""
CREATE TABLE IF NOT EXISTS {auth_table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    policy ENUM({policy}) NOT NULL,
    scope ENUM({scope}) NOT NULL,
    account VARCHAR(50) NOT NULL,
    delete_flag BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (account) REFERENCES {user_table_name}(account)
);
"""
                # UserAuth 테이블 생성
                cursor.execute(create_auth_table_query)
                connection.commit()

        except Exception as ex:
            # 트랜잭션 롤백
            connection.rollback()
            raise ex

        finally:
            # 연결 닫기
            connection.close()

    def delete_user(self):
        connection = self.connect()
        user_table_name = self.get_padding_name("user")
        auth_table_name = self.get_padding_name("user_auth")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 삭제 쿼리
                drop_table_query = f"DROP TABLE IF EXISTS {auth_table_name};"
                cursor.execute(drop_table_query)

                # "users" 테이블 삭제 쿼리
                drop_table_query = f"DROP TABLE IF EXISTS {user_table_name};"
                cursor.execute(drop_table_query)

                # 변경 사항을 커밋
                connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def check_exist_user(self) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("user")
        ret = False
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블이 존재하는지 확인하는 쿼리 실행
                table_exists_query = f"SHOW TABLES LIKE '{table_name}';"
                cursor.execute(table_exists_query)

                # 결과 가져오기
                result = cursor.fetchone()

                if result:
                    ret = True
        finally:
            # 연결 닫기
            connection.close()
            return ret