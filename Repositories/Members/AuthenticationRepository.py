import __init__
from abc import ABCMeta, abstractmethod
from typing import Optional
from result import Result

from Domains.Members import *


class IVerifiableAuthentication(metaclass=ABCMeta):
    @abstractmethod
    def identify_and_authenticate(
        self, account: str, passwd: str
    ) -> Result[Authentication, str]:
        """_summary_

        Args:
            account (str): _description_
            passwd (str): _description_

        Returns:
            Result[Authentication, str]:
                Ok(Authentication) : Contains information about the login and its success or failure.
                Err(str) : Represents errors in storage, if any, as a string.
        """
        ...

    @abstractmethod
    def update_access(self, auth: Authentication) -> Result[None, str]:
        """_summary_
        Update last_access with the current time, and Update the fail_count according to the successes and failures.

        Args:
            auth (Authentication): Use the value returned by identify_and_authenticate as is.

        Returns:
            Result[None, str]:
                Err(str) : Represents errors in storage, if any, as a string.
        """
        ...
