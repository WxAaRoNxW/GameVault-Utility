def validate_steam_id(id: str):
    try:
        id = int(id)
    except:
        id = 0
    if id <= 76561202255233023 and id >= 76561197960265728:
        return True
    return False