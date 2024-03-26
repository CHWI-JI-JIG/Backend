import __init__
from datetime import datetime, timedelta

from Domains.Sessions.ISession import SecuritySession


def check_valide_session(session: SecuritySession) -> bool:
    assert issubclass(
        type(session), SecuritySession
    ), "session must inherit from SecuritySession"

    if session.create_time + timedelta(minutes=session.VALIDE_MINUTE()) < datetime.now():
        return False
    if session.get_use_count() >= session.MAX_USE_COUNT():
        return False

    return True
