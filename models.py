from dataclasses import dataclass

@dataclass
class Bar:
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    index: int = 0
    time: str = ""

@dataclass 
class Box:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

@dataclass
class Line:
    def __init__(self, _x1, _y1, _x2, _y2):
        self.x1 = _x1
        self.x2 = _x2
        self.y2 = _y2
        self.y1 = _y1

# @dataclass
# class Liquidity:
#     def __init__(self, level, start_index, broken, bx, bz):
#         self.level: float = level
#         self.start_index: int = start_index
#         self.broken: bool = broken
#         self.bx : Box = bx
#         self.bz : Box = bz

@dataclass
class Liquidity:
    
        level: float = None
        start_index: int =None
        start_bar : Bar = None
        broken: bool = None
        bx : Box = None
        bz : Box = None

@dataclass
class ZZ:
    def __init__(self):
        self.direction: list[int] = [0 for i in range(50)]
        self.x: list[int] = [0 for i in range(50)]
        self.y: list[float] = [None for i in range(50)]

    def in_and_out(self, _d: int, _i: int, _p: float):
        self.direction.insert(0, _d)
        self.x.insert(0, _i)
        self.y.insert(0, _p)

