import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional, List, Tuple
from result import Result, Err, Ok

from Domains.Comments import *
from Repositories.Comments import *
from Builders.Members import *
from Builders.Comments import *
from uuid import UUID

from Domains.Products import *
from Repositories.Products import *
from Builders.Products import *

import pymysql

from icecream import ic


class MySqlGetComment(IGetableComment):
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

    def get_comments_by_product_id(
        self,
        product_id: ProductID,
        page=0,
        size=10,
    ) -> Result[Tuple[int, List[Comment]], str]:

        connection = self.connect()
        comment_table_name = self.get_padding_name("comments")
        member_table_name = self.get_padding_name("user")
        try:
            # 커서 생성
            with connection.cursor() as cursor:
                offset = page * size
                query = f"""
SELECT comment.id, comment.writer_id, user.account, comment.question, comment.answer, comment.product_id
FROM {comment_table_name} AS comment
    INNER JOIN {member_table_name} AS user
    ON comment.writer_id = user.id
WHERE comment.product_id = %s
LIMIT %s, %s;
"""               
                cursor.execute(query, (product_id, offset, size))
                result = cursor.fetchall()

                comments = []
                for row in result:
                    id, product_id, writer_id, writer_account, answer, question = row
                    comment = Comment(
                        id=CommentIDBuilder().set_uuid(id).build(),
                        writer_id=writer_id,
                        writer_account=writer_account,
                        answer=answer,
                        question=question,
                        product_id=product_id,
                    )
                    comments.append(comment)
                cursor.execute(f"SELECT COUNT(*) FROM {comment_table_name}")
                total_count = cursor.fetchone()[0]

                connection.commit()
                return Ok((total_count, comments))

        except Exception as e:
            connection.close()
            return Err(str(e))
