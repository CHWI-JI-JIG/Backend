import __init__

from Domains.Members import RoleType
from datetime import datetime

def hashing_passwd(
    password: str,
) -> str:
    import hashlib

    hash = hashlib.sha256()
    hash.update(password.encode("utf-8"))
    return hash.hexdigest()


def check_passwd_change(last_changed_date: datetime, role: RoleType) -> bool:
    """
    비밀번호 변경이 필요한지 확인하는 함수
    """
    assert isinstance(last_changed_date, datetime), "Type of date is datetime"
    assert isinstance(role,RoleType), "Type of role is RoleType"
    
    current_date = datetime.now()
    if role == RoleType.ADMIN:
        days_to_check = 90  # 180 = 6 months(반기)
    else:
        days_to_check = 60  # 60 days
    # days_since_last_change = (current_date - last_changed_date).days
    # return days_since_last_change > days_to_check
    
    # 테스트 시 아래 코드 사용
    time_since_last_change = current_date - last_changed_date
    return time_since_last_change.total_seconds() > days_to_check