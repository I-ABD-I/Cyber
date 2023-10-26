div7 = [n for n in range(1, 101) if n % 7 == 0]

has3 = [n for n in range(1, 101) if "3" in str(n)]


def countspaces(s: str) -> int:
    return len([c for c in s if c == " "])


def notvowels(s: str) -> list:
    return [c for c in s if c not in "aeiou AEIOU"]


def common(list_a: list, list_b: list) -> list:
    return [x for x in list_a if x in list_b]


def numbers(s: str) -> list:
    return [n for n in s.split() if n.isnumeric()]


def shortwords(s: str) -> list:
    return [w for w in s.split() if len(w) < 4]
