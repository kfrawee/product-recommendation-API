from typing import Dict, List, Union


def translate_keys_or_values(
    data: Union[Dict, List],
    mapping: Dict = dict(),
    keys: bool = True,
    translate_only: str = None,
    reverse: bool = False,
) -> Union[Dict, List]:
    """
    Translate data keys/
    params:
    data: (Dict or List) Data to be replaced
    mapping: (Dict) Dictionary of Mappings to use
      column names as keys and English column names as values
    keys: (bool) To translate keys or values
    translate_only: (str) value to translate only. Incase of same kays' values
    reverse: (bool) To reverse used mapping (keys with values)
    return:
    Translated data: Union[Dict, List]
    """
    if not data:
        return None
    if reverse:
        mapping = {v: k for k, v in mapping.items()}

    if isinstance(data, list):
        new_data = [mapping.get(d) for d in data]
        # remove empty values
        new_data = [d for d in new_data if d]
    else:
        new_data = {}
        if keys:
            for k, v in data.items():
                if k in mapping:
                    if translate_only:
                        if k == translate_only:
                            new_data[mapping[k]] = v
                    else:
                        new_data[mapping[k]] = v
                else:
                    new_data[k] = v
        else:
            for k, v in data.items():
                if v in mapping:
                    if translate_only:
                        if v == translate_only:
                            new_data[k] = mapping[v]
                    else:
                        new_data[k] = mapping[v]
                else:
                    new_data[k] = v

    return new_data


def convert_values_to_string(data: Dict) -> Dict:
    for k, v in data.items():
        data[k] = str(v)
    return data
