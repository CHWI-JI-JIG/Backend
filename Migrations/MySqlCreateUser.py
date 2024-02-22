import __init__
import pymysql

from icecream import ic


class MySqlCreateUser:
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

        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 생성 쿼리
                create_user_table_query = f"""
CREATE TABLE IF NOT EXISTS {user_table_name} (
    seq INT AUTO_INCREMENT PRIMARY KEY,
    id VARCHAR(255) UNIQUE,
    account VARCHAR(255) UNIQUE,
    pay_account VARCHAR(255),
    passwd VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    company_registration_number VARCHAR(255),
    phone VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_access DATETIME NOT NULL DEFAULT '1900-01-01 01:01:01',
    fail_count INT NOT NULL DEFAULT 0
);
                """
                print(create_user_table_query)
                # user 생성
                cursor.execute(create_user_table_query)
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
        try:
            # 커서 생성
            with connection.cursor() as cursor:
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
        
        
    
