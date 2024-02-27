import __init__

from flask import Flask, session, jsonify, request
from Applications.Members.CreateMemberService import CreateMemberService
from Applications.Members.LoginMemberService import AuthenticationMemberService
from get_config_data import get_db_padding
from icecream import ic

from Storages.Members.MySqlSaveMember import  MySqlSaveMember
from Storages.Members.LoginVerifiableAuthentication import LoginVerifiableAuthentication
from Storages.Sessions.MakeSaveMemberSession import MakeSaveMemberSession
from result import Result, Ok, Err
from Domains.Sessions import MemberSession

import sys
from pathlib import Path

SECRETSPATH = __init__.root_path/"secrets.json"

with SECRETSPATH.open('r') as f:
    secrets = jsonify.load(f)

app = Flask(__name__)
app.secret_key = secrets['SECRET_KEY']

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
            return jsonify({'success': True, 'certification' : 'true','key': member_session.get_id(), 'auth' : str(member_session.role.name), 'name': str(member_session.name)}), 200
        case Err(e):
            return jsonify({'success': False}), 401

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
