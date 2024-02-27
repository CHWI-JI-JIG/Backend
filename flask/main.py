import __init__

from flask import Flask, session, jsonify, request
#from Applications.Members.CreateMemberService import CreateMemberService
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



app = Flask(__name__)
app.secret_key = "zxcvqwer"

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
            return jsonify({'success': 'true', 'certification' : 'true','key': member_session.get_id(), 'auth' : str(member_session.role.name), 'name': str(member_session.name)}), 200
        case Err(e):
            return jsonify({'success': 'false'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
