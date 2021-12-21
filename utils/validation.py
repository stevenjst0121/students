def is_id_valid(id: str) -> bool:
    if type(id) != str or len(id) != 18:
        return False

    return True


def is_name_valid(name: str) -> bool:
    if type(name) != str or not name:
        return False

    for _char in name:
        if not "\u4e00" <= _char <= "\u9fa5":
            return False
    return True
