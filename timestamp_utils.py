from datetime import datetime


def utc_timestamp():
    return datetime.utcnow().isoformat()
