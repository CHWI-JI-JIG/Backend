# member_view.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Applications.Members.CreateMemberService import CreateMemberService
from Domains.Members import Privacy
from get_config_data import get_db_padding
from icecream import ic
import json

# MySqlSaveMember 클래스 import 추가
from Storages.Members.MySqlSaveMember import MySqlSaveMember


def signup(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method is required'}, status=405)
    
    data = json.loads(request.body.decode('utf-8'))

    # 데이터 파싱
    account = data.get('id')
    passwd = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')

    # role 설정
    role = "buyer" # 구매자라면, 사업자 번호 / 계좌번호가 없어야 하고 
    # 판매자라면, 사업자 번호 / 계좌번호가 있어야 하고 

    # 의존성 주입
    save_member_repo = MySqlSaveMember(get_db_padding())
    member_service = CreateMemberService(save_member_repo)

    # 회원 가입 시도
    result = member_service.create(account, passwd, role, name, phone, email, address)
    ic(result)
    # 결과에 따른 응답 생성
    if result.is_ok():
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def signup_b(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method is required'}, status=405)
    
    data = json.loads(request.body.decode('utf-8'))

    # 데이터 파싱
    account = data.get('userId')
    passwd = data.get('userPassword')
    name = data.get('userName')
    phone = data.get('userPhone')
    email = data.get('userEmail')
    address = data.get('userAddress')
    pay_account = data.get('userBankAccount')
    

    # role 설정
    role = "seller" # 구매자라면, 사업자 번호 / 계좌번호가 없어야 하고 
    company_registration_number = "123-45-67890"
 

    # 의존성 주입
    save_member_repo = MySqlSaveMember(get_db_padding())
    member_service = CreateMemberService(save_member_repo)

    # 회원 가입 시도
    result = member_service.create(account, passwd, role, name, phone, email, address, pay_account, company_registration_number)
    ic(result)
    # 결과에 따른 응답 생성
    if result.is_ok():
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

# def check_session_login(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'POST method is required'}, status=405)
    
#     data = json.loads(request.body.decode('utf-8'))

#     # 데이터 파싱
#     account = data.get('userId')
#     passwd = data.get('userName')
#     name = data.get('email')
#     phone = data.get('login')
#     email = data.get('auth')
    

#     # role 설정
#     role = "seller" # 구매자라면, 사업자 번호 / 계좌번호가 없어야 하고 
#     company_registration_number = "123-45-67890"
 

#     # 의존성 주입
#     save_member_repo = MySqlSaveMember(get_db_padding())
#     member_service = CreateMemberService(save_member_repo)

#     # 회원 가입 시도
#     result = member_service.create(account, passwd, role, name, phone, email, address, pay_account, company_registration_number)
#     ic(result)
#     # 결과에 따른 응답 생성
#     if result.is_ok():
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False})

