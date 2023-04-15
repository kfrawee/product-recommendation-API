from typing import Dict, List


def translate_keys(
    data: Dict = dict(), mapping: Dict = dict(), reverse: bool = False
) -> Dict:
    """
    Translate data keys/
    params:
    data: (Dict) Data to be replaced
    mapping: (Dict) Dictionary of Mappings to use
      column names as keys and English column names as values
    reverse: (bool) To reverse used mapping (keys with values)
    return:
    Dict
    """
    if not data:
        return data

    new_data = {}
    if reverse:
        mapping = {v: k for k, v in mapping.items()}

    for k, v in data.items():
        if k in mapping:
            new_data[mapping[k]] = v
        else:
            new_data[k] = v

    return new_data
