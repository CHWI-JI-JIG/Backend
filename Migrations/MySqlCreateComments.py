import __init__
import pymysql

from icecream import ic


class MySqlCreateComments:
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

    def create_comments(self):
        connection = self.connect()
        comments_table_name = self.get_padding_name("comments")
        user_table_name = self.get_padding_name("user")
        product_table_name = self.get_padding_name("product")

        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "comments" 테이블 생성 쿼리
                create_comments_table_query = f"""
CREATE TABLE IF NOT EXISTS {comments_table_name} (
    id VARCHAR(255) UNIQUE,
    contents VARCHAR(255) NOT NULL,
    recomments VARCHAR(255),
    writer_id VARCHAR(255),
    product_id VARCHAR(255),
    FOREIGN KEY (writer_id) REFERENCES {user_table_name}(id),
    FOREIGN KEY (product_id) REFERENCES {product_table_name}(id)
    );
                """
                # user 생성
                cursor.execute(create_comments_table_query)
                connection.commit()

        except Exception as ex:
            # 트랜잭션 롤백
            connection.rollback()
            raise ex

        finally:
            # 연결 닫기
            connection.close()

    def delete_comments(self):
        connection = self.connect()
        comments_table_name = self.get_padding_name("comments")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                # "users" 테이블 삭제 쿼리
                drop_table_query = f"DROP TABLE IF EXISTS {comments_table_name};"
                cursor.execute(drop_table_query)

                # 변경 사항을 커밋
                connection.commit()

        finally:
            # 연결 닫기
            connection.close()

    def check_exist_comments(self) -> bool:
        connection = self.connect()
        table_name = self.get_padding_name("comments")
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
