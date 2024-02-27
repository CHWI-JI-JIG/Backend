import sys
from pathlib import Path

now_path = Path(__file__).resolve().parent
root_path = now_path.parent.parent

if not (str(root_path) in sys.path):
    sys.path.append(str(root_path))

from Domains.Members.MemberID import (
    MemberID,
    IMemberIDBuilder,
)

from Domains.Members.Member import (
    Member,
    RoleType,
    IMemberBuilder,
)

from Domains.Members.Privacy import (
    Privacy,
    IPrivacyBuilder,
)

from Domains.Members.Authentication import (
    Authentication,
    IAuthenticationBuilder,
)


__all__ = [
    "MemberID",
    "IMemberIDBuilder",
    "Member",
    "IMemberBuilder",
    "Privacy",
    "IPrivacyBuilder",
    "Authentication",
    "IAuthenticationBuilder",
    "RoleType",
]
