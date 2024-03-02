import __init__

from flask import Flask, session, jsonify, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from Applications.Members.CreateMemberService import CreateMemberService
from Applications.Members.LoginMemberService import AuthenticationMemberService
from Applications.Members.AdminService import AdminService
from Applications.Products.ReadProductService import ReadProductService
from Applications.Products.CreateProductService import CreateProductService
from Applications.Orders.ReadOrderService import ReadOrderService
from get_config_data import get_db_padding
from icecream import ic

from Storages.Members.MySqlEditMember import  MySqlEditMember
from Storages.Members.MySqlGetMember import  MySqlGetMember
from Storages.Members.MySqlSaveMember import  MySqlSaveMember
from Storages.Orders.MySqlGetOrder import MySqlGetOrder
from Storages.Products import MySqlSaveProduct
from Storages.Members.LoginVerifiableAuthentication import LoginVerifiableAuthentication
from Storages.Sessions import *
from Storages.Products.MySqlGetProduct import MySqlGetProduct
from result import Result, Ok, Err
from Domains.Orders import *
from Domains.Sessions import MemberSession
from Domains.Products import *
from mysql_config import mysql_db

import os
import sys
import math
from pathlib import Path
import json
from flask_cors import CORS

import pymysql

SECRETSPATH = __init__.root_path/"secrets.json"
IMG_PATH = __init__.root_path/"Images"
#ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif'}


with SECRETSPATH.open('r') as f:
    secrets = json.load(f)

app = Flask(__name__)
CORS(app)
app.secret_key = secrets['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = IMG_PATH

#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/api/Images/<path:filename>')
def send_image(filename): #/Images/img102.png
    ic(filename)
    return (send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    
@app.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', type=str)
    keyword = '%'+keyword+'%'
    
    db = pymysql.connect(**mysql_db)
    
    page = request.args.get('page', type=int)
    page -= 1
    totalCount = 0
    totalPage = 0
    size = 20
    
    
    try:
        with db.cursor() as cursor:
            
            sql = f"SELECT COUNT(*) as count FROM {get_db_padding()}product WHERE name LIKE %s"
            cursor.execute(sql, (keyword,))
            result = cursor.fetchone()
            ic(result)
            if result and isinstance(result[0], int):
                totalCount = result[0]
                totalPage = math.ceil(totalCount/size)
            ic(totalCount)
            offset = page * size
            sql = f"SELECT * FROM {get_db_padding()}product WHERE name LIKE %s LIMIT %s, %s"
            cursor.execute(sql, (keyword,offset, size))
            rows = cursor.fetchall()
            data = []
            for row in rows:
                temp_data = {
                    "sellerId": row[0],
                    "productId": row[1],
                    "seq": row[2],
                    "productName": row[3],
                    "productImageUrl":url_for('send_image', filename=row[4]), # /Images/image1.jpg
                    #'http://serveraddr/Images'+ v.img_path,
                    "productPrice": row[5],
                    "productDescription": row[6],
                    "date": row[7]
                }
                data.append(temp_data)
    finally:
        db.close()
        
    response = {
        "page": page+1,
        "totalPage" : totalPage,
        "totalCount" : totalCount,
        "size" : size,
        "data" : data
        
    }
    
    return jsonify(response)

@app.route('/api/product-registration', methods = ['POST'])
def productRegistration():
    
    if 'file' not in request.files:
            return jsonify({"error": "Invalid image file."}), 400
    
    # data = request.get_json()
    # ic(data)
    # memberAuth = data.get('key')
    # #tempProductId = data.get('tempProductId')
    # productImagePath = data.get("file")
    # productName = data.get('productName')
    # productPrice = data.get('productPrice')
    # productDescription = data.get('productDescription')
    #productRegistrationData = data.get('productRegistrationData')
    #sellerId = data.get('sellerId')
    
    productName = request.form['productName']
    productPrice = int(request.form['productPrice'])
    productDescription = request.form['productDescription']
    memberAuth = request.form.get('key')
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    member_save_repo = MySqlSaveMember(get_db_padding())
    save_product=MySqlSaveProduct(get_db_padding())
    save_product_session=MySqlSaveProductTempSession(get_db_padding())
    load_session=MySqlLoadSession(get_db_padding())
    
    regi = CreateProductService(save_product, save_product_session,load_session)
    check = regi.publish_temp_product_id(memberAuth)
    
    match check:
        case Ok(member_session):
            check = member_session
        case _:
            return jsonify({'success' : False})
            
    regiImg = regi.check_upload_image_path(file.filename, check.get_id())
    match regiImg:
        case Ok(member_session):
            pass
            # regiImg = member_session
        case _:
            return jsonify({'success': False})
    
    productInfo = regi.upload_product_data(productName, productPrice, productDescription, check.get_id())
    match productInfo:
        case Ok(member_session):
            pass
            # productInfo = member_session
        case _:
            return jsonify({'success': False})
        
    result = regi.create(check.get_id())
    match result:
        case Ok(member_session):
            return jsonify({'success': True})
        case Err(e):
            return jsonify({'success': False})

@app.route('/api/detail', methods = ['GET'] )
def detail():
    productId = request.args.get('productId', type=str)
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    get_product_detail_info = ReadProductService(get_product_repo, load_session_repo)
    result = get_product_detail_info.get_product_for_detail_page(productId)
    
    match result:
        case None:
            jsonify({'success': False})
        case ret if isinstance(ret, Product):
            res_data = {
                "productId" : ret.id.get_id(),
                "productName" : ret.name,
                "productDescription" : ret.description,
                "productPrice" : ret.price,
                "productImageUrl" : url_for('send_image', filename=ret.img_path)
            }
            return jsonify(res_data)
    
    
@app.route('/api/products', methods=['GET'])
def product():
    
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    get_product_info = ReadProductService(get_product_repo, load_session_repo)
    
    page = request.args.get('page', type=int)
    page -= 1
    size = 20
    result = get_product_info.get_product_data_for_main_page(page, size)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, products)):
            
            response_data["totalPage"] = math.ceil(max/size)
            for v in products:
                product_data = {
                    "productId" : str (v.id.get_id()),
                    "sellerId" : str(v.seller_id.get_id()),
                    "productName" : v.name,
                    "productImageUrl" : url_for('send_image', filename=v.img_path), # /Images/image1.jpg
                    #'http://serveraddr/Images'+ v.img_path
                    "productPrice" : v.price
                }
                response_data["data"].append(product_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})     

@app.route('/api/sproducts', methods=['POST'])
def sellerProduct():
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    get_product_info = ReadProductService(get_product_repo, load_session_repo)
    
    data = request.get_json()
    user_key = data.get('key')
    page = data.get('page')
    page -= 1

    size = 20
    result = get_product_info.get_product_data_for_seller_page( user_key, page, size)
    ic(result)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, products)):
            
            response_data["totalPage"] = math.ceil(max/size)
            for v in products:
                ic(products)
                product_data = {
                    "productId" : str (v.id.get_id()),
                    "productName" : v.name,
                    "productImageUrl" : url_for('send_image', filename=v.img_path), # /Images/image1.jpg
                    #'http://serveraddr/Images'+ v.img_path,
                    "productPrice" : v.price,
                    "regDate" : v.register_day
                }
                response_data["data"].append(product_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})     

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    userId = data.get('userId')
    userPassword = data.get('userPassword')

    auth_member_repo = LoginVerifiableAuthentication(get_db_padding())
    session_repo = MakeSaveMemberSession(get_db_padding())

    login_pass = AuthenticationMemberService(auth_member_repo, session_repo)
    result = login_pass.login(userId, userPassword)

    match result:
        case Ok(member_session):
            
            ic(member_session)
            session['key'] = member_session.get_id()
            session['auth'] = member_session.role.name
            
            return jsonify({'success': True, 'certification' : True,'key': member_session.get_id(), 'auth' : str(member_session.role.name), 'name': str(member_session.name)}), 200
        case Err(e):
            return jsonify({'success': False})

@app.route('/api/check-id', methods=['GET'])
def check_id():
    id = request.args.get('id', default='', type=str)
    duplicated = check_id_duplicate(id)
    return jsonify({'duplicated': duplicated})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    account = data.get('buyerId')
    passwd = data.get('buyerPassword')
    role = "buyer"
    name = data.get('buyerName')
    phone = data.get('buyerPhone')
    email = data.get('buyerEmail')
    address = data.get('buyerAddress')
    
    
    save_member_repo = MySqlSaveMember(get_db_padding())
    member_service = CreateMemberService(save_member_repo)
    
    result = member_service.create(account, passwd, role, name, phone, email, address)
    
    if result.is_ok():
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False})
    
@app.route('/api/b-signup', methods=['POST'])
def bsignup():
    data = request.get_json()
    
    account = data.get('sellerId')
    passwd = data.get('sellerPassword')
    role = "seller"
    name = data.get('sellerName')
    phone = data.get('sellerPhone')
    email = data.get('sellerEmail')
    address = data.get('sellerAddress')
    company_registration_number = data.get('sellerBRN')
    pay_account = data.get('sellerBankAccount')
    
    save_member_repo = MySqlSaveMember(get_db_padding())
    member_service = CreateMemberService(save_member_repo)
    
    result = member_service.create(account, passwd, role, name, phone, email, address, company_registration_number, pay_account)
    
    if result.is_ok():
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False})
    
## susujin code
@app.route('/api/admin', methods=['POST'])
def adminUser():
    read_repo = MySqlGetMember(get_db_padding())
    edit_repo = MySqlEditMember(get_db_padding())
    
    get_user_info = AdminService(read_repo, edit_repo)
    
    data = request.get_json()
    user_key = data.get('key')
    page = data.get('page')
    page -= 1

    size = 20
    result = get_user_info.read_members(page, size)
    ic(result)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, members)):
            response_data["totalPage"] = math.ceil(max/size)
            for v in members:
                ic(members)
                user_data = {
                    "userKey" : str (v.id.get_id()), #사용자 key
                    "userId" : v.account, #사용자 아이디(로그인용)
                    "userAuth" : v.role #사용자 권한

                }
                response_data["data"].append(user_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})
        
@app.route('/api/user-role', methods=['POST'])
def updateUserRole():
    read_repo = MySqlGetMember(get_db_padding())
    edit_repo = MySqlEditMember(get_db_padding())
    
    get_user_info = AdminService(read_repo, edit_repo)
    
    data = request.get_json()
    user_key = data.get('key') # 세션키(즉, 관리자 세션키)
    user_id = data.get('userKey') # 사용자 key
    new_role = data.get('userAuth')  # 변경할 권한

    result = get_user_info.change_role(new_role, user_id)
    ic(result)

    match result:
        case Ok(user_id):
            return jsonify({'success': True, 'message': 'User role updated successfully'})

        case Err(e):
            return jsonify({'success': False, 'message': str(e)})
## susujin code end

## susujin code
@app.route('/api/admin', methods=['POST'])
def adminUser():
    read_repo = MySqlGetMember(get_db_padding())
    edit_repo = MySqlEditMember(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    
    get_user_info = AdminService(read_repo, edit_repo, load_session_repo)
    
    data = request.get_json()
    user_key = data.get('key')
    page = data.get('page')
    page -= 1

    size = 20
    result = get_user_info.read_members(page, size)
    ic(result)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, members)):
            response_data["totalPage"] = math.ceil(max/size)
            for v in members:
                ic(members)
                user_data = {
                    "key" : v.id,
                    "userId" : v.account,
                    "userAuth" : v.role

                }
                response_data["data"].append(user_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})
        
@app.route('/api/user-role', methods=['POST'])
def updateUserRole():
    read_repo = MySqlGetMember(get_db_padding())
    edit_repo = MySqlEditMember(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    get_user_info = AdminService(read_repo, edit_repo)
    
    data = request.get_json()
    #user_key = data.get('key')
    user_id = data.get('key')  # 사용자 UUID
    new_role = data.get('userAuth')  # 변경할 권한

    result = get_user_info.change_role(new_role, user_id, load_session_repo)
    ic(result)

    match result:
        case Ok(user_id):
            return jsonify({'success': True, 'message': 'User role updated successfully'})

        case Err(e):
            return jsonify({'success': False, 'message': str(e)})
## susujin code end

@app.route('/api/order-histroy', methods = ['POST'])
def orderHistroy():
    get_order_Repo=MySqlGetOrder(get_db_padding())
    load_session_repo=MySqlLoadSession(get_db_padding())
    
    get_order_info=ReadOrderService(get_order_Repo, load_session_repo)
    
    data = request.get_json()
    user_id = data.get('key')
    page = data.get('page')
    page -= 1
    size = 20
    
    result = get_order_info.get_order_data_for_buyer_page(user_id,page,size)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, members)):
            response_data["totalPage"] = math.ceil(max/size)
            for v in members:
                ic(members)
                order_data = {
                    "productId" : v.product_id,
                    "productName" : v.product_name,
                    "productImageUrl" : v.product_img_path,
                    "orderQuantity" : v.buy_count,
                    "orderPrice" : v.total_price,
                    "orderDate" : v.order_date
                }
                response_data["data"].append(order_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})
        
        
@app.route('/api/seller-order', methods = ['POST'])
def sellerOrder():
    get_order_Repo=MySqlGetOrder(get_db_padding())
    load_session_repo=MySqlLoadSession(get_db_padding())
    
    get_order_info=ReadOrderService(get_order_Repo, load_session_repo)
    
    data = request.get_json()
    user_id = data.get('key')
    page = data.get('page')
    page -= 1
    size = 20
    
    result = get_order_info.get_order_data_for_seller_page(user_id,page,size)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, members)):
            response_data["totalPage"] = math.ceil(max/size)
            for v in members:
                ic(members)
                order_data = {
                    "buyerId" : v.buyer_id,
                    "buyerName" : v.recipient_name,
                    "byuerPhoneNumber" : v.recipient_phone,
                    "buyerAddr" : v.recipient_address,
                    "productId" : v.product_id,
                    "productName" : v.product_name,
                    "productImageUrl" : v.product_img_path,
                    "orderQuantity" : v.buy_count,
                    "orderPrice" : v.total_price,
                    "orderDate" : v.order_date
                }
                response_data["data"].append(order_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
    

    
