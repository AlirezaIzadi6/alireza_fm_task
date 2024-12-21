def is_valid_id(value):
    if value is None or not value.isdigit():
        return False
    return True