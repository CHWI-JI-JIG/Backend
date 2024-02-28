import __init__

from flask import Flask, session, jsonify, request
from Applications.Members.CreateMemberService import CreateMemberService
from Applications.Members.LoginMemberService import AuthenticationMemberService
from Applications.Products.ReadProductService import ReadProductService
from get_config_data import get_db_padding
from icecream import ic

from Storages.Members.MySqlSaveMember import  MySqlSaveMember
from Storages.Members.LoginVerifiableAuthentication import LoginVerifiableAuthentication
from Storages.Sessions.MakeSaveMemberSession import MakeSaveMemberSession
from Storages.Sessions.MySqlLoadSession import MySqlSaveSession
from Storages.Products.MySqlGetProduct import MySqlGetProduct
from result import Result, Ok, Err
from Domains.Sessions import MemberSession
from mysql_config import mysql_db

import sys
import math
from pathlib import Path
import json
from flask_cors import CORS

import pymysql

SECRETSPATH = __init__.root_path/"secrets.json"

with SECRETSPATH.open('r') as f:
    secrets = json.load(f)

app = Flask(__name__)
CORS(app)
app.secret_key = secrets['SECRET_KEY']

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
    
    data = []
    
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
            data = cursor.fetchall()
    finally:
        db.close()
        
    response = {
        'page': page+1,
        'totalPage' : totalPage,
        'totalCount' : totalCount,
        'size' : size,
        'data' : data
        
    }
    
    return jsonify(response)

@app.route('/api/products', methods=['get'])
def product():
    
    get_product_repo = MySqlGetProduct(get_db_padding())
    load_session_repo = MySqlSaveSession(get_db_padding())
    
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
                    "productImgUrl" : v.img_path,
                    "productPrice" : v.price
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
