import sys
import os
from time import sleep

os.system("")

if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios
    OLD_SETTINGS = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

STATUS_SUCCESS = 0
STATUS_ERROR   = 1
def quit(status = STATUS_SUCCESS):
    if os.name != 'nt': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, OLD_SETTINGS)
    exit(status)

def __func__():
    pass
func = type(__func__)

class Point:
    def __init__(self, y = 0, x = 0):
        self.y = y
        self.x = x
    
    def __repr__(self) -> str:
        return f"({self.y}, {self.x})"
    
    def __add__(self, p):
        return Point(self.y + p.y, self.x + p.x)
    
    def __iadd__(self, p):
        self.y += p.y
        self.x += p.x
        return self
        
    def __radd__(self, p):
        return self.__add__(p)
        
    def __sub__(self, p):
        return Point(self.y - p.y, self.x - p.x)
    
    def __isub__(self, p):
        self.y -= p.y
        self.x -= p.x
        return self
        
    def __rsub__(self, p):
        return self.__sub__(p)
        
    def __eq__(self, p):
        return (self.y, self.x) == (p.y, p.x)
    
    def __ne__(self, p):
        return (self.y, self.x) != (p.y, p.x)
    
    def __gt__(self, p):
        return (self.y, self.x) > (p.y, p.x)
    
    def __lt__(self, p):
        return (self.y, self.x) < (p.y, p.x)
    
    def __ge__(self, p):
        return (self.y, self.x) > (p.y, p.x)
    
    def __le__(self, p):
        return (self.y, self.x) < (p.y, p.x)
        
class __RenderQueue:
    def __init__(self, queue = {}):
        self.__queue: dict[tuple[int, int]] = queue

    def __repr__(self):
        return str(self.__queue)
    
    def __str__(self):
        return str(self.__queue)

    def __add__(self, rq):
        return RenderQueue(self.__queue + rq.queue)

    def __iadd__(self, rq):
        self.__queue += rq.asDict()
        
    def __radd__(self, rq):
        return self.__add__(rq)
    
    def asDict(self):
        return self.__queue

    def points(self):
        return [Point(p.y, p.x) for p in self.__queue.keys()]
    
    def get(self, point):
        return self.__queue.get((point.y, point.x))
    
    def add(self, point, symbol):
        self.__queue[(point.y, point.x)] = symbol

    def clear(self):
        self.__queue = {}

KEY_SPACE = ' '
__KEY__ = None
def key_pressed(key: str) -> bool:
    global __KEY__
    if os.name == 'nt':
        if msvcrt.kbhit():
            try:
                __KEY__ = msvcrt.getch().decode('utf-8')
            except:
                pass
    else:
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            __KEY__ = sys.stdin.read(1)
    if __KEY__ == key:
        __KEY__ = None
        return True
    return False

LINES = 0
def puts(s, overwrite = True):
    global LINES
    if '\n' in s and overwrite:
        LINES += 1
    sys.stdout.write(s)
        
Y_SIZE = 0
X_SIZE = 0
UPDATE_FN: func
SETUP_FN: func
TICKDELAY = 0
INITIALIZED = False

def init(yx_size: tuple[int, int], setup: func, update: func, tickdelay: float = 0.08):
    global Y_SIZE, X_SIZE, SETUP_FN, UPDATE_FN, TICKDELAY, INITIALIZED
    Y_SIZE = yx_size[0]
    X_SIZE = yx_size[1]
    UPDATE_FN = update
    SETUP_FN = setup
    TICKDELAY = tickdelay
    
    INITIALIZED = True

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
    for y in range(0, Y_SIZE):
        for x in range(0, X_SIZE):
            symbol = RenderQueue.get(Point(y, x))
            if symbol:
                puts(symbol)
            else:
                puts('.')
        puts('\n')   
     
def Gameloop():
    global LINES
    
    if not INITIALIZED:
        raise ValueError("Please run 'tengine.init' first!")
    
    SETUP_FN()

    while True:
        Display()
    
        UPDATE_FN()
        
        puts(f"\033[{LINES}A\r")
        LINES = 0
        sleep(TICKDELAY)