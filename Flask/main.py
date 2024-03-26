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
from result import Result, Ok, Err

from Applications.Members import *
from Applications.Products import *
from Applications.Orders import *
from Applications.Comments import *
from Applications.Payments import *
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

from get_config_data import get_db_padding
from mysql_config import mysql_db


SECRETSPATH = __init__.root_path / "secrets.json"
IMG_PATH = __init__.root_path / "Images"
ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg", "gif"}


with SECRETSPATH.open("r") as f:
    secrets = json.load(f)

app = Flask(__name__)
CORS(app)
app.secret_key = secrets["SECRET_KEY"]
app.config["UPLOAD_FOLDER"] = IMG_PATH

PG_SERVER = PaymentService()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_id_duplicate(account):
    db = pymysql.connect(**mysql_db)

    try:
        with db.cursor() as cursor:
            sql = f"SELECT account FROM {get_db_padding()}user WHERE account = %s"
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
    finally:
        db.close()

    if result:
        return True
    else:
        return False


@app.route("/api/Images/<path:filename>")
def send_image(filename):  # /Images/img102.png
    if allowed_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    else:
        return "File not allowed", 403


@app.route("/api/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword", type=str)
    keyword = "%" + keyword + "%"

    db = pymysql.connect(**mysql_db)

    page = request.args.get("page", type=int)
    page -= 1
    totalCount = 0
    totalPage = 0
    size = 20

    try:
        with db.cursor() as cursor:

            sql = f"SELECT COUNT(*) as count FROM {get_db_padding()}product WHERE name LIKE %s"
            cursor.execute(sql, (keyword,))
            result = cursor.fetchone()
            if result and isinstance(result[0], int):
                totalCount = result[0]
                totalPage = math.ceil(totalCount / size)
            offset = page * size
            sql = f"SELECT * FROM {get_db_padding()}product WHERE name LIKE %s LIMIT %s, %s"
            cursor.execute(sql, (keyword, offset, size))
            rows = cursor.fetchall()
            data = []
            for row in rows:
                temp_data = {
                    "sellerId": row[0],
                    "productId": row[1],
                    "seq": row[2],
                    "productName": row[3],
                    "productImageUrl": url_for("send_image", filename=row[4]),
                    "productPrice": row[5],
                    "productDescription": row[6],
                    "date": row[7],
                }
                data.append(temp_data)
    finally:
        db.close()

    response = {
        "page": page + 1,
        "totalPage": totalPage,
        "totalCount": totalCount,
        "size": size,
        "data": data,
    }

    return jsonify(response)


@app.route("/api/product-registration", methods=["POST"])
def productRegistration():

    if "file" not in request.files:
        return jsonify({"error": "Invalid image file."}), 400

    productName = request.form["productName"]
    productPrice = int(request.form["productPrice"])
    productDescription = request.form["productDescription"]
    memberAuth = request.form.get("key")

    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    save_product = MySqlSaveProduct(get_db_padding())
    save_product_session = MySqlSaveProductTempSession(get_db_padding())
    load_session = MySqlLoadSession(get_db_padding())

    regi = CreateProductService(save_product, save_product_session, load_session)
    check = regi.publish_temp_product_id(memberAuth)

    match check:
        case Ok(member_session):
            check = member_session
        case _:
            return jsonify({"success": False})

    regiImg = regi.check_upload_image_path(file.filename, check.get_id())
    match regiImg:
        case Ok(member_session):
            pass
            # regiImg = member_session
        case _:
            return jsonify({"success": False})

    productInfo = regi.upload_product_data(
        productName, productPrice, productDescription, check.get_id()
    )
    match productInfo:
        case Ok(member_session):
            pass
            # productInfo = member_session
        case _:
            return jsonify({"success": False})

    result = regi.create(check.get_id())
    match result:
        case Ok(member_session):
            return jsonify({"success": True})
        case Err(e):
            return jsonify({"success": False})


@app.route("/api/detail", methods=["GET"])
def detail():
    productId = request.args.get("productId", type=str)
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_product_detail_info = ReadProductService(get_product_repo, load_session_repo)
    result = get_product_detail_info.get_product_for_detail_page(productId)

    match result:
        case None:
            jsonify({"success": False})
        case ret if isinstance(ret, Product):
            res_data = {
                "productId": ret.id.get_id(),
                "productName": ret.name,
                "productDescription": ret.description,
                "productPrice": ret.price,
                "productImageUrl": url_for("send_image", filename=ret.img_path),
            }
            return jsonify(res_data)


@app.route("/api/products", methods=["GET"])
def product():

    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_product_info = ReadProductService(get_product_repo, load_session_repo)

    page = request.args.get("page", type=int)
    page -= 1
    size = 20
    result = get_product_info.get_product_data_for_main_page(page, size)
    response_data = {"page": page + 1, "size": size, "data": []}

    match result:
        case Ok((max, products)):

            response_data["totalPage"] = math.ceil(max / size)
            for v in products:
                product_data = {
                    "productId": v.id.get_id(),
                    "sellerId": v.seller_id.get_id(),
                    "productName": v.name,
                    "productImageUrl": url_for("send_image", filename=v.img_path),
                    "productPrice": v.price,
                }
                response_data["data"].append(product_data)
            return jsonify(response_data)

        case Err(e):
            ic(e)
            return jsonify({"success": False})


@app.route("/api/sproducts", methods=["POST"])
def sellerProduct():
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_product_info = ReadProductService(get_product_repo, load_session_repo)

    data = request.get_json()
    user_key = data.get("key")
    page = data.get("page")
    page -= 1

    size = 20
    result = get_product_info.get_product_data_for_seller_page(user_key, page, size)
    response_data = {"page": page + 1, "size": size, "data": []}

    match result:
        case Ok((max, products)):

            response_data["totalPage"] = math.ceil(max / size)
            for v in products:
                product_data = {
                    "productId": v.id.get_id(),
                    "productName": v.name,
                    "productImageUrl": url_for("send_image", filename=v.img_path),
                    "productPrice": v.price,
                    "regDate": v.register_day,
                }
                response_data["data"].append(product_data)
            return jsonify(response_data)

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    userId = data.get("userId")
    userPassword = data.get("userPassword")

    auth_member_repo = MySqlLoginAuthentication(get_db_padding())
    session_repo = MySqlMakeSaveMemberSession(get_db_padding())
    load_repo = MySqlLoadSession(get_db_padding())
    del_session_repo = MySqlDeleteSession(get_db_padding())

    login_pass = AuthenticationMemberService(
        auth_member_repo, session_repo, load_repo, del_session_repo
    )
    result = login_pass.login(userId, userPassword)

    match result:
        case Ok((member_session, changePw)):

            ic(member_session)
            session["key"] = member_session.get_id()
            session["auth"] = member_session.role.name
            ic(changePw)

            return (
                jsonify(
                    {
                        "success": True,
                        "certification": True,
                        "key": member_session.get_id(),
                        "auth": member_session.role.name,
                        "changePw": changePw,
                        "name": member_session.name,
                    }
                ),
                200,
            )
        case Err(e):
            return jsonify({"success": False})


@app.route("/api/change-pw", methods=["POST"])
def changeExpiredPw():
    pass_repo = MySqlChangePasswd(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    auth_member_repo = MySqlLoginAuthentication(get_db_padding())

    change = ChangePasswdService(pass_repo, load_session_repo, auth_member_repo)

    data = request.get_json()
    user_key = data.get("key")  # 세션키
    old_passwd = data.get("password")
    new_passwd = data.get("newPassword")

    result = change.change_expired_pw(user_key, old_passwd, new_passwd)

    match result:
        case Ok(_):
            return jsonify({"success": True}, 200)
        case Err("만료된 세션입니다"):
            return jsonify({"success": False, "msg":"만료된 세션입니다"})
        case Err(e):
            return jsonify({"success": False})


@app.route("/api/check-id", methods=["GET"])
def check_id():
    id = request.args.get("id", default="", type=str)
    duplicated = check_id_duplicate(id)
    return jsonify({"duplicated": duplicated})


@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    account = data.get("buyerId")
    passwd = data.get("buyerPassword")
    role = "buyer"
    name = data.get("buyerName")
    phone = data.get("buyerPhone")
    email = data.get("buyerEmail")
    address = data.get("buyerAddress")

    save_member_repo = MySqlSaveMember(get_db_padding())
    member_service = CreateMemberService(save_member_repo)

    result = member_service.create(account, passwd, role, name, phone, email, address)

    if result.is_ok():
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False})


@app.route("/api/b-signup", methods=["POST"])
def bsignup():
    data = request.get_json()

    account = data.get("sellerId")
    passwd = data.get("sellerPassword")
    role = "seller"
    name = data.get("sellerName")
    phone = data.get("sellerPhone")
    email = data.get("sellerEmail")
    address = data.get("sellerAddress")
    company_registration_number = data.get("sellerBRN")
    pay_account = data.get("sellerBankAccount")

    save_member_repo = MySqlSaveMember(get_db_padding())
    member_service = CreateMemberService(save_member_repo)

    ic(account)
    result = member_service.create(
        account,
        passwd,
        role,
        name,
        phone,
        email,
        address,
        company_registration_number,
        pay_account,
    )

    if result.is_ok():
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False})


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

        case Err("만료된 세션입니다"):
            return jsonify({"success": False, "msg":"만료된 세션입니다"})
        case Err(e):
            return jsonify({"success": False, "message": str(e)})

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
    result = get_user_info.read_members(user_key, page, size)

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

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/order-history", methods=["POST"])
def orderHistroy():
    get_order_Repo = MySqlGetOrder(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_order_info = ReadOrderService(get_order_Repo, load_session_repo)

    data = request.get_json()
    user_id = data.get("key")
    page = data.get("page")
    page -= 1
    size = 3

    ic(user_id, page, size)

    result = get_order_info.get_order_data_for_buyer_page(user_id, page, size)
    response_data = {"page": page + 1, "size": size, "data": []}

    match result:
        case Ok((max, product)):
            response_data["totalPage"] = math.ceil(max / size)
            response_data["totalCount"] = max
            for v in product:
                order_data = {
                    "productId": v.product_id.get_id(),
                    "productName": v.product_name,
                    "productImageUrl": url_for(
                        "send_image", filename=v.product_img_path
                    ),
                    "orderQuantity": v.buy_count,
                    "orderPrice": v.total_price,
                    "orderDate": v.order_date,
                }
                response_data["data"].append(order_data)
            return jsonify(response_data)

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/seller-order", methods=["POST"])
def sellerOrder():
    get_order_Repo = MySqlGetOrder(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    get_order_info = ReadOrderService(get_order_Repo, load_session_repo)

    data = request.get_json()
    user_id = data.get("key")
    page = data.get("page")
    page -= 1
    size = 20

    result = get_order_info.get_order_data_for_seller_page(user_id, page, size)
    response_data = {"page": page + 1, "size": size, "data": []}

    match result:
        case Ok((max, members)):
            response_data["totalPage"] = math.ceil(max / size)
            for v in members:
                order_data = {
                    "buyerId": v.buyer_id.get_id(),
                    "buyerName": v.recipient_name,
                    "buyerPhoneNumber": v.recipient_phone,
                    "buyerAddr": v.recipient_address,
                    "productId": v.product_id.get_id(),
                    "productName": v.product_name,
                    "productImageUrl": url_for(
                        "send_image", filename=v.product_img_path
                    ),
                    "orderQuantity": v.buy_count,
                    "orderPrice": v.total_price,
                    "orderDate": v.order_date,
                }
                response_data["data"].append(order_data)
            return jsonify(response_data)

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/userproductinfo", methods=["POST"])
def userProductInfo():
    save_order = MySqlSaveOrder(get_db_padding())
    save_transition = MySqlSaveOrderTransition(get_db_padding())
    load_session = MySqlLoadSession(get_db_padding())
    get_product = MySqlGetProduct(get_db_padding())

    save_trans_info = OrderPaymentService(
        save_order, save_transition, load_session, get_product
    )

    data = request.get_json()

    user_session_key = data.get("key")
    recipient_name = data.get("userName")
    recipient_phone = data.get("userPhone")
    recipient_address = data.get("userAddr")
    product_id = data.get("productId")
    product_name = data.get("productName")
    buy_count = data.get("productCount")
    single_price = data.get("productPrice")

    result = save_trans_info.publish_order_transition(
        recipient_name=recipient_name,
        recipient_phone=recipient_phone,
        recipient_address=recipient_address,
        product_id=product_id,
        buy_count=buy_count,
        single_price=single_price,
        user_session_key=user_session_key,
    )

    match result:
        case Ok(session):
            return jsonify({"success": True, "transId": session.get_id()})
        case Err("만료된 세션입니다"):
            return jsonify({"success": False, "msg":"만료된 세션입니다"})

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/PG/sendpayinfo", methods=["POST"])
def sendPayInfo():
    save_order = MySqlSaveOrder(get_db_padding())
    save_transition = MySqlSaveOrderTransition(get_db_padding())
    load_session = MySqlLoadSession(get_db_padding())
    get_product = MySqlGetProduct(get_db_padding())

    send_pay_info = OrderPaymentService(
        save_order, save_transition, load_session, get_product
    )

    data = request.get_json()

    order_transition_session = data.get("key")
    card_num = data.get("cardNum")
    total_price = data.get("productPrice")
    payment_success = data.get("paymentVerification")

    match PG_SERVER.approval_and_logging(
        order_transition_session, total_price, card_num
    ):
        case Ok(True):
            pass
        case e:
            msg = "결제 실패"
            if e.is_err():
                msg = e.err()
            ic(e, msg)
            return jsonify({"success": False, "msg": msg})

    match send_pay_info.payment_and_approval_order(
        order_transition_session=order_transition_session,
        payment_success=True,
    ):
        case Ok(_):
            return jsonify({"success": True})

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/answer", methods=["POST"])
def qaAnswer():
    save_comment = MySqlSaveComment(get_db_padding())
    load_session = MySqlLoadSession(get_db_padding())

    add_answer_info = CreateCommentService(save_comment, load_session)

    data = request.get_json()

    answer = data.get("answer")
    comment_id = data.get("qId")
    user_key = data.get("key")

    match add_answer_info.add_answer(answer, comment_id, user_key):
        case Ok(_):
            return jsonify({"success": True})

        case Err("만료된 세션입니다"):
            return jsonify({"success": False, "msg":"만료된 세션입니다"})
        case Err(e):
            return jsonify({"success": False, "message": str(e)})


@app.route("/api/qa", methods=["POST"])
def qaLoad():
    get_comment_repo = MySqlGetComment(get_db_padding())
    qa_load_info = ReadCommentService(get_comment_repo)
    data = request.get_json()
    product_id = data.get("productId")

    if product_id is None:
        return jsonify({"success": False, "error": "Product ID is missing"})

    page = data.get(
        "page", 1
    )  # 페이지가 제공되지 않았거나 유효하지 않은 경우 기본값으로 1을 사용합니다.
    size = 10

    result = qa_load_info.get_comment_data_for_product_page(product_id, page - 1, size)
    response_data = {"page": page, "size": size, "data": []}

    match result:
        case Ok((max, comments)):
            response_data["totalPage"] = math.ceil(max / size)
            for v in comments:
                comment_data = {
                    "productId": v.product_id.get_id(),
                    "qId": v.id.get_id(),
                    "buyerKey": v.writer_id.get_id(),
                    "buyerId": v.writer_account,
                    "question": v.question,
                    "answer": v.answer,
                }
                response_data["data"].append(comment_data)
            return jsonify(response_data)

        case Err(e):
            return jsonify({"success": False})


@app.route("/api/qa-question", methods=["POST"])
def qaQuestion():
    save_comment = MySqlSaveComment(get_db_padding())
    load_session = MySqlLoadSession(get_db_padding())

    create_qa_info = CreateCommentService(save_comment, load_session)

    data = request.get_json()

    question = data.get("question")
    user_key = data.get("key")
    product_id = data.get("productId")

    match create_qa_info.create_question(question, product_id, user_key):
        case Ok(_):
            return jsonify({"success": True})
        case Err("만료된 세션입니다"):
            return jsonify({"success": False, "msg":"만료된 세션입니다"})
        case Err(e):
            ic(e)
            return jsonify({"success": False, "msg":e})


@app.route("/api/c-user", methods=["POST"])
def cUser():
    read_repo = MySqlGetPrivacy(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())

    c_user_info = ReadPrivacyService(read_repo, load_session_repo)

    data = request.get_json()

    user_session_key = data.get("key")

    result = c_user_info.read_privacy(user_session_key)

    match result:
        case Ok(privacy):
            privacy_data = {
                "userId": privacy.id.get_id(),
                "userName": privacy.name,
                "userPhone": privacy.phone,
                "userAddr": privacy.address,
            }
            return jsonify(privacy_data)
        case Err("만료된 세션입니다"):
            return jsonify({"success": False, "msg":"만료된 세션입니다"})

        case Err(e):
            return jsonify({"success": False})


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
        return jsonify({"success": False})


@app.route("/api/err-test")
def err_test():
    res = jsonify({"message": "Internal Server Error"})
    res.status_code = 500
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
