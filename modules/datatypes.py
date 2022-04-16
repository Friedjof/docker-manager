# Friedjof Noweck
# 2022-04-13 Mi

import numpy as np


class Unsigned16BitInt:
    def __init__(self, nr: int):
        self._nr: int = np.array([nr], dtype="uint16")[0]

    def __int__(self) -> int:
        return self._nr

    def __str__(self) -> str:
        return f"{self._nr}"


if __name__ == '__main__':
    u16Int: Unsigned16BitInt = Unsigned16BitInt(65535)

    print(u16Int)
