import __init__
import pymysql

from icecream import ic


class MySqlCreateSession:
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

    def create_session(self):
        connection = self.connect()
        session_table_name = self.get_padding_name("session")

        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 생성 쿼리
                create_session_table_query = f"""
CREATE TABLE IF NOT EXISTS {session_table_name} (
    seq INT AUTO_INCREMENT PRIMARY KEY,
    id VARCHAR(255) UNIQUE NOT NULL,
    value VARCHAR(500) NOT NULL  
);
                """
                print(create_session_table_query)
                # session 생성
                cursor.execute(create_session_table_query)
                connection.commit()

        except Exception as ex:
            # 트랜잭션 롤백
            connection.rollback()
            raise ex

        finally:
            # 연결 닫기
            connection.close()

    def delete_session(self):
        connection = self.connect()
        session_table_name = self.get_padding_name("session")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 삭제 쿼리
                drop_table_query = f"DROP TABLE IF EXISTS {session_table_name};"
                cursor.execute(drop_table_query)

                # 변경 사항을 커밋
                connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def check_exist_session(self) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("session")
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
