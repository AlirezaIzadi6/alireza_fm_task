from file_manager.constants.size import BYTE, KILOBYTE, MEgABYTE

def get_readable_size(size_in_bytes: int) -> str:
    if size_in_bytes < KILOBYTE:
        return f'{size_in_bytes}B'
    elif size_in_bytes < MEgABYTE:
        return f'{round(size_in_bytes/KILOBYTE, 2)}KB'
    else:
        return f'{round(size_in_bytes/MEgABYTE, 2)}MB'