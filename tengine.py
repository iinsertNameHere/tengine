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

def __func__():
    pass
func = type(__func__)

STATUS_SUCCESS = 0
STATUS_ERROR   = 1
def quit(status = STATUS_SUCCESS):
    if os.name != 'nt': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, OLD_SETTINGS)
    exit(status)

LINES = 0
def puts(s, overwrite = True):
    global LINES
    if '\n' in s and overwrite:
        LINES += 1
    sys.stdout.write(s)
 
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
        
    
        
Y_SIZE = 0
X_SIZE = 0
UPDATE: func
SETUP: func
TICKDELAY = 0

INITIALIZED = False
def init(yx_size: tuple[int, int], setup: func, update: func, tickdelay: float = 0.08):
    global Y_SIZE, X_SIZE, SETUP, UPDATE, TICKDELAY, INITIALIZED
    Y_SIZE = yx_size[0]
    X_SIZE = yx_size[1]
    UPDATE = update
    SETUP = setup
    TICKDELAY = tickdelay
    
    INITIALIZED = True

RENDER_POINTS: dict[Point, str] = {}
def Add_RenderPoint(p: Point, ch: str):
    global RENDER_POINTS
    RENDER_POINTS[(p.y, p.x)] = ch

def Get_RenderPoints() -> list[Point]:
    return [Point(p.y, p.x) for p in RENDER_POINTS.keys()]

def Clear_RenderPoints():
    global RENDER_POINTS
    RENDER_POINTS = {}

def DISPLAY():
    for y in range(0, Y_SIZE):
        for x in range(0, X_SIZE):
            current_point = (y, x)
            if current_point in RENDER_POINTS.keys():
                puts(RENDER_POINTS[current_point])
            else:
                puts('.')
        puts('\n')   
     
def Gameloop():
    global LINES
    
    if not INITIALIZED:
        raise ValueError("Please run 'tengine.init' first!")
    
    SETUP()

    while True:
        DISPLAY()
    
        UPDATE()
        
        puts(f"\033[{LINES}A\r")
        LINES = 0
        sleep(TICKDELAY)