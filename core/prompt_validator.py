import uuid

def validate_steam_id(id: str):
    try:
        id = int(id)
    except:
        id = 0
    if id <= 76561202255233023 and id >= 76561197960265728:
        return True
    return False

def validator_uuid(uuid_to_test: str):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
        return str(uuid_obj) == uuid_to_test
    except ValueError:
        return False

def validate_prompt(validator_type: str):
    match validator_type:
        case "uuid":
            return validator_uuid
        case "steam_id":
            return validate_steam_id
        case _:
            return None