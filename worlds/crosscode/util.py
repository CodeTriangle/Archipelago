"""
Everyone's favorite part of every python library: miscellaneous utility functions anc classes.
"""

import functools
import typing

K = typing.TypeVar("K")
V = typing.TypeVar("V")

class KeyDefaultDict(dict[K, V]):
    """
    Like defaultdict, but bases the default value on the key.
    """
    default_factory: typing.Callable[[K], V] | None
    """
    Function that takes a key and returns that key's default value.
    """

    def __init__(
       self,
       default_factory: typing.Callable[[K], V],
       *args: typing.Iterable[typing.Any],
       **kwargs: dict[str, typing.Any]
    ):
        """
        Creates a keydefaultdict with the specified factory function. Remaining arguments are sent to the dict 
        """
        self.default_factory = default_factory
        super().__init__(*args, **kwargs)

    def __missing__(self, key: K):
        """
        Runs when a dict value is missing.
        """
        if self.default_factory is None:
            raise KeyError( key )
        ret = self[key] = self.default_factory(key)
        return ret

def maximum_gap(counter: list[int]) -> int:
    """
    Calculates the maximum number of consecutive elements in a list that are zero.
    """

    # in the tuple, the first element represents the current largest known gap
    # and the second element represents the gap that is currently being calculated
    def gapfun(t: tuple[int, int], d: int) -> tuple[int, int]:
        return (max(t[0], t[1] + 1), t[1] + 1) if not d else (t[0], 0)

    return functools.reduce(
        gapfun,
        counter,
        initial=(0, 0)
    )[0]
