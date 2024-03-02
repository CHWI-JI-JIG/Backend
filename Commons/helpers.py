def check_hex_string(s:str)->bool:
    assert isinstance(s, str)
    import re
    hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
    return bool(hex_pattern.match(s))   