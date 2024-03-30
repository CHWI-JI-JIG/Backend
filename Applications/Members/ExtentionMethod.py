import __init__

from typing import List, Tuple
from Domains.Members.Member import RoleType
from datetime import datetime, timedelta

def hashing_passwd(
    password: str,
) -> str:
    import hashlib

    hash = hashlib.sha256()
    hash.update(password.encode("utf-8"))
    return hash.hexdigest()


def get_block_time(num_of_incorrect_login: int) -> int:
    """_summary_
    틀린 횟수에 따른 정지시간을 관리한다.
    Args:
        num_of_incorrect (int): _description_

    Returns:
        int: 제한 하는 분 반환 / 제한을 하지 않으면 0반환
    """
    #
    block_rule_list: List[Tuple[int, int]] = [
        (5, 5),  # 5회 틀리면, 5분
        (7, 30),  # 7회 틀리면 30분
        (9, 60),  # 9회 틀리면 1시간
        (11, 1440),  # 11회 틀리면 하루
        (13, 4320),  # 13회 틀리면 3일
    ]
    max_block: Tuple[int, int, int] = (
        15,
        2,
        10080,
    )  # 15회 이후부터는 2번 틀릴때마다 일주일씩 블락
    for threshold, block_time in block_rule_list:
        if num_of_incorrect_login == threshold:
            return block_time

    # 횟수가 최대 횟수를 초과하는 경우 최대 정지 시간 적용
    match num_of_incorrect_login - max_block[0]:
        case minus if minus < 0:  # not max
            return 0
        case up_max:
            return ((up_max + 1) % max_block[1]) * max_block[2]

def check_login_able(last_access: datetime, block_minute: int) -> bool:
    """
    로그인 가능 여부를 확인하는 함수
    """
    # 잠긴 상태에서 시간이 지난 경우 잠금 해제
    if last_access + timedelta(minutes=block_minute) < datetime.now():
        return True
    else:
        return False

def check_passwd_change(last_changed_date: datetime, role: RoleType) -> bool:
    """
    비밀번호 변경이 필요한지 확인하는 함수
    """
    assert isinstance(last_changed_date, datetime), "Type of date is datetime"
    assert isinstance(role,RoleType), "Type of role is RoleType"
    
    current_date = datetime.now()
    if role == RoleType.ADMIN:
        days_to_check = 180  # 180 = 6 months(반기)
    else:
        days_to_check = 60  # 60 days
    days_since_last_change = (current_date - last_changed_date).days
    return days_since_last_change > days_to_check
    
    # 테스트 시 아래 코드 사용
    # time_since_last_change = current_date - last_changed_date
    # return time_since_last_change.total_seconds() > days_to_check

