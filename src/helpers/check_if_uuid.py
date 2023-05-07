import uuid


def is_valid_uuid(uuid_to_check):
    try:
        uuid.UUID(str(uuid_to_check))

        return True
    except ValueError:
        return False
