from typing import Callable


isNumeric: Callable[[str], bool] = lambda s: s.isnumeric()

multiply = lambda x, y: x * y

sort: Callable[[list[tuple[str, int]]], list] = lambda t: sorted(t, key=lambda x: x[1])
