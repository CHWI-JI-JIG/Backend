import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result, Err, Ok

from Domains.Comments import *
from Repositories.Comments import *
from Builders.Members import *
from uuid import UUID

import pymysql

from icecream import ic


class MySqlSaveComment(ISaveableComment):
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

    def save_comment(self, comment: Comment) -> Result[UUID, str]:
            connection = self.connect()
            comment_table_name = self.get_padding_name("comments")
            member_table_name = self.get_padding_name("user")
            try:
                # 커서 생성
                with connection.cursor() as cursor:
                    insert_query = f"""
    INSERT INTO {comment_table_name} (
        id,
        answer,
        question,
        writer_id,
        product_id
    ) VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        insert_query,
                        (
                            comment.id.get_id(),
                            comment.answer,
                            comment.question,
                            comment.writer_id, 
                            comment.product_id,
                        ),
                    )
                    # 변경 사항을 커밋
                    connection.commit()
                    return Ok(comment.id.uuid)
            except Exception as e:
                connection.rollback()
                return Err(str(e))
            finally:
                connection.close()