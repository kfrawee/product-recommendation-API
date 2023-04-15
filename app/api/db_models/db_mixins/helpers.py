import json


def json_loader(obj):
    try:
        data = json.loads(obj)
        return data
    except Exception:
        return {}


def arr_loader(obj):
    try:
        data = json.loads(obj)
        return data
    except Exception:
        return []
