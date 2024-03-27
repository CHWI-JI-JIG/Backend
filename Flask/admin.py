import __init__

from flask import (
    Flask,
    session,
    jsonify,
    request,
    redirect,
    url_for,
    send_from_directory,
)

from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import random
import os
import sys
import math
from pathlib import Path
import json
from flask_cors import CORS

import pymysql

from icecream import ic
from typing import Dict
from result import Result, Ok, Err

from Applications.Members import *
from Applications.Sessions import *

from Storages.Members import *
from Storages.Orders import *
from Storages.Products import *
from Storages.Comments import *
from Storages.Sessions import *

from Domains.Members import *
from Domains.Products import *
from Domains.Orders import *
from Domains.Comments import *
from Domains.Sessions import *

from get_config_data import get_db_padding, get_mail_object
from mysql_config import mysql_db

from datetime import datetime, timedelta


SECRETSPATH = __init__.root_path / "secrets.json"
auth_member_repo = MySqlLoginAuthentication(get_db_padding())
session_repo = MySqlMakeSaveMemberSession(get_db_padding())
otp_session_repo = TempMySqlMakeSaveMemberSession(get_db_padding())
otp_load_session_repo = TempMySqlLoadSession(get_db_padding())
load_repo = MySqlLoadSession(get_db_padding())
del_session_repo = MySqlDeleteSession(get_db_padding())

login_service = LoginAdminService(
    auth_member_repo,
    session_repo,
    load_repo,
    del_session_repo,
    otp_session_repo,
    otp_load_session_repo,
)


app = Flask(__name__)
CORS(app)
app.config["SESSION_REFRESH_EACH_REQUEST"] = False

app.config.from_object(get_mail_object())
mail = Mail(app)
otp_storage: Dict[str, str] = {}


def generate_otp():
    return random.randint(100000, 999999)


def get_create_time_by_key(key):
    # 데이터베이스 연결 설정
    conn = pymysql.connect(**mysql_db)

    try:
        with conn.cursor() as cursor:
            # id 값이 key와 일치하는 행의 create_time 값을 조회하는 SQL 쿼리
            sql = "SELECT create_time FROM log_otp WHERE id = %s"
            cursor.execute(sql, (key,))
            result = cursor.fetchone()

            if result:
                return result[0]  # create_time 값 반환
            else:
                return None  # 일치하는 행이 없는 경우
    finally:
        conn.close()


def send_otp_email(email, otp):
    message = Message(
        "Your OTP", sender=get_mail_object().MAIL_USERNAME, recipients=[email]
    )
    message.body = f"Your OTP is: {otp}"
    mail.send(message)


@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    data = request.json
    key = data.get("key")
    if not key:
        return jsonify({"error": "Key is required"}), 400

    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    create_time = get_create_time_by_key(key)

    otp = generate_otp()
    ic(otp)
    send_otp_email(email, otp)

    otp_storage["otp"] = str(otp)
    return "OTP sent!"


@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    user_otp = request.json.get("otp")
    key: str = request.json.get("key")

    current_time = datetime.now()
    otp_key = otp_storage.get("otp")
    ic(otp_key, user_otp)

    if not otp_key:
        return "Session expired or invalid!", 400

    create_time = get_create_time_by_key(key)

    expiration_time = create_time + timedelta(minutes=10)
    ic(expiration_time)

    if current_time <= expiration_time:
        if otp_key == user_otp:
            match login_service.otp_login(key):
                case Ok(user_seeeeion):
                    return jsonify(
                        {
                            "success": True,
                            "key": user_seeeeion.get_id(),
                            "auth": str(user_seeeeion.role.name),
                            "message": "OTP 인증 완료",
                        }
                    )
                case e:
                    ic(e)
                    return jsonify({"success": False, "message": "로그인 실패"})
        else:
            return jsonify({"success": False, "message": "OTP 인증 실패"})
    else:
        return jsonify({"success": False, "message": "OTP 기간 만료"})


@app.route("/api/login", methods=["POST"])
@app.route("/api/Adminlogin", methods=["POST"])
def Adminlogin():
    data = request.get_json()

    userId = data.get("userId")
    userPassword = data.get("userPassword")
    ic(userId)
    ic(userPassword)

    result = login_service.login(userId, userPassword)
    ic(result)
    match result:
        case Ok(member_session):
            response_data = {
                "key": member_session.get_id(),
            }
            ic(response_data)

            conn = pymysql.connect(**mysql_db)
            try:
                # 커서 생성
                with conn.cursor() as cursor:
                    sql = "SELECT email FROM log_user WHERE role = 'admin'"
                    cursor.execute(sql)

                    admin_email = cursor.fetchone()

                    if admin_email:
                        # response_data['success'] = True
                        # response_data['email'] = admin_email[0]
                        print(admin_email[0])
                        response_data["success"] = True
                        response_data["email"] = admin_email[0]

                    else:
                        jsonify(
                            {
                                "success": False,
                                "message": "Admin 정보를 찾을 수 없습니다.",
                            }
                        )
            finally:
                conn.close()

            return (jsonify(response_data), 200)
        case e:
            ic(e)
            return jsonify({"success": False, "message": "잘못된 접근입니다."})


@app.route("/api/admin", methods=["POST"])
def adminUser():
    read_repo = MySqlGetMember(get_db_padding())
    edit_repo = MySqlEditMember(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_user_info = AdminService(read_repo, edit_repo, load_session_repo)

    data = request.get_json()
    user_key = data.get("key")
    page = data.get("page")
    page -= 1

    size = 20
    ic(user_key, page)
    result = get_user_info.read_members(user_key, page, size)
    ic(result)

    response_data = {"page": page + 1, "size": size, "data": []}

    match result:
        case Ok((max, members)):
            response_data["totalPage"] = math.ceil(max / size)
            for v in members:
                user_data = {
                    "userKey": v.id.get_id(),  # 사용자 key
                    "userId": v.account,  # 사용자 아이디(로그인용)
                    "userAuth": v.role.value,  # 사용자 권한
                }
                response_data["data"].append(user_data)
            return jsonify(response_data)

        case e:
            ic(e)
            return jsonify({"success": False, "message": "잘못된 접근입니다."})


@app.route("/api/user-role", methods=["POST"])
def updateUserRole():
    read_repo = MySqlGetMember(get_db_padding())
    edit_repo = MySqlEditMember(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_user_info = AdminService(read_repo, edit_repo, load_session_repo)

    data = request.get_json()
    user_key = data.get("key")  # 세션키(즉, 관리자 세션키)
    user_id = data.get("userKey")  # 사용자 key
    new_role = data.get("userAuth")  # 변경할 권한

    result = get_user_info.change_role(user_key, new_role, user_id)

    match result:
        case Ok(user_id):
            return jsonify(
                {"success": True, "message": "User role updated successfully"}
            )

        case e:
            ic(e)
            return jsonify({"success": False, "message": "잘못된 접근입니다."})


@app.route("/api/logout", methods=["POST"])
def logout():

    data = request.get_json()

    user_key = data.get("key")

    del_session_repo = MySqlDeleteSession(get_db_padding())
    logout = MemberSessionService(del_session_repo)

    result = logout.logout(user_key)

    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "message": "잘못된 접근입니다."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)
