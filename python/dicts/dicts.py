DICT = {"Theodore": 19, "Roxanne": 20, "Mathew": 21, "Betty": 20}

# list of keys:
keys = DICT.keys()

# list of values:
[*values] = DICT.values()

# key of max value
[*DICT.keys()][[*DICT.values()].index(max(DICT.values()))]


def dict_to_tuple(dict: dict) -> list[tuple]:
    return [*dict.items()]


def list_to_dict(list1, list2) -> dict:
    return dict(zip(list1, list2))


def get_keys(dict: dict, value) -> list:
    return [k for k, v in dict.items() if v == value]


def combine_dicts(dict1: dict, dict2: dict) -> dict:
    combined = {k: [v] for k, v in dict1.items()}
    for k, v in dict2.items():
        combined.setdefault(k, []).append(v)

    return combined


def int_part(lst: list[float]) -> dict[int, list[float]]:
    IF_dict: dict[int, list[float]] = {}
    for i in lst:
        IF_dict.setdefault(int(i), [i]).append(i)
    return IF_dict
