import __init__


def hashing_passwd(
    password: str,
) -> str:
    import hashlib

    hash = hashlib.sha256()
    hash.update(password.encode("utf-8"))
    return hash.hexdigest()
