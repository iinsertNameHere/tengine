import sys
import os
from time import sleep
from enum import IntEnum

os.system("")

if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios
    OLD_SETTINGS = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

class Status(IntEnum):
    SUCCESS = 0
    ERROR   = 1

def quit(status: Status = Status.SUCCESS):
    if os.name != 'nt': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, OLD_SETTINGS)
    exit(status)

def __func__():
    pass
func = type(__func__)

class Point:
    def __init__(self, y: int = 0, x: int = 0):
        self.y = y
        self.x = x
    
    def __repr__(self) -> str:
        return f"({self.y}, {self.x})"
    
    def __add__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return Point(self.y + p.y, self.x + p.x)
    
    def __iadd__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        self.y += p.y
        self.x += p.x
        return self
        
    def __radd__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return self.__add__(p)
        
    def __sub__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return Point(self.y - p.y, self.x - p.x)
    
    def __isub__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        self.y -= p.y
        self.x -= p.x
        return self
        
    def __rsub__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return self.__sub__(p)
        
    def __eq__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.y, self.x) == (p.y, p.x)
    
    def __ne__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.y, self.x) != (p.y, p.x)
    
    def __gt__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.y, self.x) > (p.y, p.x)
    
    def __lt__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.y, self.x) < (p.y, p.x)
    
    def __ge__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.y, self.x) > (p.y, p.x)
    
    def __le__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.y, self.x) < (p.y, p.x)
    
    def dup(self):
        """
            Returns a duplicate of itself
        """
        return Point(self.y, self.x)
        
class __RenderQueue:
    def __init__(self, queue: dict = {}):
        self.__queue: dict[tuple[int, int]] = queue

    def __repr__(self) -> str:
        return str(self.__queue)
    
    def __str__(self) -> str:
        return str(self.__queue)

    def __add__(self, rq):
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        return RenderQueue(self.__queue + rq.queue)

    def __iadd__(self, rq):
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        self.__queue += rq.asDict()
        
    def __radd__(self, rq):
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        return self.__add__(rq)
    
    def asDict(self) -> dict[tuple[int, int], str]:
        return self.__queue

    def points(self) -> list[Point]:
        return [Point(p.y, p.x) for p in self.__queue.keys()]
    
    def get(self, point) -> str|None:
        return self.__queue.get((point.y, point.x))
    
    def add(self, point: Point, symbol: str):
        self.__queue[(point.y, point.x)] = symbol

    def clear(self):
        self.__queue = {}

KEY_SPACE = ' '
__KEY = None
def key_pressed(key: str) -> bool:
    global __KEY
    if os.name == 'nt':
        if msvcrt.kbhit():
            try:
                __KEY = msvcrt.getch().decode('utf-8')
            except:
                pass
    else:
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            __KEY = sys.stdin.read(1)
    if __KEY == key:
        __KEY = None
        return True
    return False

__LINES = 0
def puts(s: str, overwrite: bool = True):
    global __LINES
    if '\n' in s and overwrite:
        __LINES += 1
    sys.stdout.write(s)
        
Y_SIZE = 0
X_SIZE = 0
__UPDATE_FN: func
__SETUP_FN: func
__TICKDELAY = 0
__BG_SYMBOL: str
__BORDER: bool
__INITIALIZED = False

def init(yx_size: tuple[int, int], setup: func, update: func, tickdelay: float = 0.08, bg_symbol: str = '.', border: bool = True):
    global Y_SIZE, X_SIZE, __SETUP_FN, __UPDATE_FN, __TICKDELAY, __BG_SYMBOL, __BORDER, __INITIALIZED
    Y_SIZE = yx_size[0]
    X_SIZE = yx_size[1]
    __UPDATE_FN = update
    __SETUP_FN = setup
    __TICKDELAY = tickdelay
    __BG_SYMBOL = bg_symbol
    __BORDER = border

    __INITIALIZED = True

RenderQueue = __RenderQueue()
def Strings2RenderQueue(lines: list[str], origin: Point):
    global RenderQueue

    lines2d = [list(l) for l in lines]
    origins = (origin, Point(origin.y + len(lines2d), origin.x + len(lines2d[0])))
    idxs = []
    points = []

    for y in range(0, origins[1].y - origins[0].y):
        for x in range(0, origins[1].x - origins[0].x):
            idxs.append(Point(y, x))

    for y in range(origins[0].y, origins[1].y):
        for x in range(origins[0].x, origins[1].x):
            points.append(Point(y, x))
    
    for i, point in enumerate(points):
        idx = idxs[i]
        ch = lines2d[idx.y][idx.x]
        RenderQueue.add(point, ch)

def Display():
    if __BORDER: puts("." + ("-"*X_SIZE) + '.\n')
    for y in range(0, Y_SIZE):
        if __BORDER: puts('|')
        for x in range(0, X_SIZE):
            symbol = RenderQueue.get(Point(y, x))
            if symbol:
                puts(symbol)
            else:
                puts(__BG_SYMBOL)
        if __BORDER: puts('|')
        puts('\n')
    if __BORDER: puts("`" + ("-"*X_SIZE) + '´\n')

def Flush():
    global __LINES
    puts(f"\033[{__LINES}A\r")
    __LINES = 0

def Gameloop():
    if not __INITIALIZED:
        raise ValueError("Please run 'tengine.init' first!")
    
    __SETUP_FN()

    while True:
        Display()
    
        __UPDATE_FN()
        
        Flush()
        sleep(__TICKDELAY)