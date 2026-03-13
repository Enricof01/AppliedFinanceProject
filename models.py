from dataclasses import dataclass

@dataclass
class Bar:
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    index: int = 0

@dataclass
class Liquidity:
    level: float = 0
    start_index: int = 0
    broken: bool = False

class ZZ:
    def __init__(self):
        self.direction: list[int] = []
        self.index: list[int] = []
        self.price: list[float] = []

    def in_and_out(self, _d: int, _i: int, _p: float):
        self.direction.insert(0, _d)
        self.index.insert(0, _i)
        self.price.insert(0, _p)

