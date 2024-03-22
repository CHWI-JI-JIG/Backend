import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import *


class IChangeablePasswd(metaclass=ABCMeta):
    @abstractmethod
    def update_passwd(self, member_id: MemberID, passwd:str) -> Result[MemberID, str]: ...