import __init__

from flask import Flask, session, jsonify, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from Applications.Members.CreateMemberService import CreateMemberService
from Applications.Members.LoginMemberService import AuthenticationMemberService
from Applications.Products.ReadProductService import ReadProductService
from Applications.Products.CreateProductService import CreateProductService
from get_config_data import get_db_padding
from icecream import ic

from Storages.Members.MySqlSaveMember import  MySqlSaveMember
from Storages.Members.LoginVerifiableAuthentication import LoginVerifiableAuthentication
from Storages.Sessions import *
from Storages.Products.MySqlGetProduct import MySqlGetProduct
from result import Result, Ok, Err
from Domains.Sessions import MemberSession
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

@app.route('/Images/<path:filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', type=str)
    keyword = '%'+keyword+'%'
    
    db = pymysql.connect(**mysql_db)
    
    page = request.args.get('page', type=int)
    page -= 1
    totalCount = 0
    totalPage = 0
    size = 3
    
    
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
                    "productImgUrl":url_for('http://192.1680.132/Images', filename=row[4]), # /Images/image1.jpg
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
    
    data = request.get_json()
    memberAuth = data.get('key')
    #tempProductId = data.get('tempProductId')
    productImagePath = data.get("productImagePath")
    productName = data.get('productName')
    productPrice = data.get('productPrice')
    productDescription = data.get('productDescription')
    #productRegistrationData = data.get('productRegistrationData')
    #sellerId = data.get('sellerId')
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    member_save_repo = MySqlSaveMember(get_db_padding())
    regi = CreateProductService(member_save_repo)
    check = regi.publish_temp_product_id(memberAuth)
    match check:
        case Ok(member_session):
            check = member_session
        case _:
            return jsonify({'success' : False})
            
    regiImg = regi.check_upload_image_path(productImagePath, check.get_id())
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

@app.route('/api/products', methods=['get'])
def product():
    
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    get_product_info = ReadProductService(get_product_repo, load_session_repo)
    
    page = request.args.get('page', type=int)
    page -= 1
    size = 3
    result = get_product_info.get_product_data_for_main_page(page, size)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, products)):
            
            response_data["totalPage"] = math.ceil(max/size)
            for v in products:
                product_data = {
                    "productId" : str (v.id.uuid),
                    "sellerId" : str(v.seller_id.uuid),
                    "productName" : v.name,
                    "productImgUrl" : url_for('http://192.1680.132/Images', filename=v.img_path), # /Images/image1.jpg
                    #'http://serveraddr/Images'+ v.img_path
                    "productPrice" : v.price
                }
                response_data["data"].append(product_data)
            return jsonify(response_data)
            
        case Err(e):
            return jsonify({'success': False})     

@app.route('/api/seller-products', methods=['POST'])
def sellerProduct():
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlLoadSession(get_db_padding())
    
    get_product_info = ReadProductService(get_product_repo, load_session_repo)
    
    data = request.get_json()
    seller_id = data.get('sellerId')
    user_key = data.get('key')
    page = data.get('page')
    page -= 1
    size = 3
    result = get_product_info.get_product_data_for_seller_page(seller_id, user_key, page, size)
    response_data = {"page":page+1, "size": size,"data": []}
    
    match result:
        case Ok((max, products)):
            
            response_data["totalPage"] = math.ceil(max/size)
            for v in products:
                product_data = {
                    "productId" : str (v.id.uuid),
                    "productName" : v.name,
                    "productImgUrl" : url_for('http://192.1680.132/Images', filename=v.img_path), # /Images/image1.jpg
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
