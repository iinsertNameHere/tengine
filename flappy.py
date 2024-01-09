import sys
import os
from time import sleep
from random import randint

if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios

os.system("")


Y = 30
X = 70
X_OFFSET = 30
X_MAX    = 40

Y_OFFSET = 8
Y_MAX    = 20

def BUILD_PLAYER_BODY():
    return [
        (PLAYER_POINT[0] - 1, PLAYER_POINT[1]),
        (PLAYER_POINT[0], PLAYER_POINT[1]),
        (PLAYER_POINT[0], PLAYER_POINT[1] + 1),
        (PLAYER_POINT[0] + 1, PLAYER_POINT[1])
    ]

def exit(e = 0):
    if os.name != 'nt': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    sys.exit(e)	

def BUILD_OBJECT_BODY(obj, d):
    body = []
    x = obj[1]
    
    if d == OBJ_UP:
        for y in range(0 - obj[0], 1):
            y = y * (-1)
            body += [(y, x - 1), (y, x), (y, x + 1)]
    elif d == OBJ_DOWN:
        for y in range(obj[0], Y):
            body += [(y, x - 1), (y, x), (y, x + 1)]
    else:
        print("Invalid object direction!")
        exit(1)
    
    return body

def BUILD_OBJECT_BODYS():
    bodys = []
    for obj_pair in OBJECTS:
        b1 = BUILD_OBJECT_BODY(obj_pair[0], OBJ_UP)
        b2 = BUILD_OBJECT_BODY(obj_pair[1], OBJ_DOWN)
        bodys += b1 + b2
    
    return bodys
        
        

PLAYER_POINT = (15, 6)
PLAYER_BODY = BUILD_PLAYER_BODY()
PLAYER_V = 0

OBJ_UP = 0
OBJ_DOWN = 1

OBJECTS = []
OBJECT_BODYS = []
OBJ_MAX = 5

__KEY__ = None     
if os.name != 'nt':
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    def is_pressed(key):
        global __KEY__
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            __KEY__ = sys.stdin.read(1)
            
        if __KEY__ == key:
            __KEY__ = None
            return True
        
        return False
else:
    def is_pressed(key):
        global __KEY__
        if msvcrt.kbhit():
            __KEY__ = msvcrt.getch().decode('utf-8')
        
        if __KEY__ == key:
            __KEY__ = None
            return True
        
        return False

def puts(s):
    sys.stdout.write(s)

def display():
    for y in range(0, Y):
        for x in range(0, X):
            if (y, x) == PLAYER_POINT:
                puts('@')
            elif (y, x) in PLAYER_BODY:
                puts('O')
            elif (y, x) in OBJECT_BODYS:
                puts('#')
            else:
                puts('.')
        puts('\n')
    
def move():
    global PLAYER_POINT, PLAYER_V, PLAYER_BODY, OBJECTS, OBJECT_BODYS

    y, x = PLAYER_POINT

    if PLAYER_V > 0:
        PLAYER_V -= 1
        PLAYER_POINT = (y - 1, x)
    elif PLAYER_V < 1:
        PLAYER_V -= 1
        PLAYER_POINT = (y + 1, x)
    else:
        print("Unknown PLAYER_V!")
        exit(1)
    
    NEW_OBJECTS = []
    for obj_pair in OBJECTS:
        obj1, obj2 = obj_pair
        
        obj1 = (obj1[0], obj1[1] - 1)
        obj2 = (obj2[0], obj2[1] - 1)
        
        if obj1[1] + 1 >= 0:
            NEW_OBJECTS.append((obj1, obj2))
    
    OBJECTS = NEW_OBJECTS
        
    PLAYER_BODY = BUILD_PLAYER_BODY()
    OBJECT_BODYS = BUILD_OBJECT_BODYS()

def spawn_object_pair():
    global OBJECTS
    
    x = X + 3
    y = randint(Y_OFFSET, Y_MAX)
    
    OBJECTS.append(((y, x), (y + 10, x)))
    
def main():
    global PLAYER_V, OBJECTS
    
    spawndelay = 0
    
    while True:
        display()
            
        for p in PLAYER_BODY:
            if p in OBJECT_BODYS:
                exit()
            
        if is_pressed('f'):
            if PLAYER_V > 0:
                PLAYER_V = 5
            else:
                PLAYER_V = 2
                
        elif is_pressed('q'):
            exit()
        
        move()
        
        if len(OBJECTS) <= OBJ_MAX and spawndelay <= 0:
            spawndelay = 30
            spawn_object_pair()
        
        if PLAYER_POINT[0] >= Y or PLAYER_POINT[0] < 0:
            exit()
        
        puts(f"\033[{Y}A\r")
        sleep(0.1)
        
        spawndelay -= 1
    
if __name__ == "__main__":
    main()
