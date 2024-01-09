import sys
import os
from time import sleep
from random import randint

if os.name == 'nt':
    import msvcrt
else:
    import select
    import termios
    import tty

os.system("")

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

STATE_GAMELOOP = 0
STATE_GAMEOVER = 1

Y = 20
X = 42

PLAYER_POINT = (3, 5)
PLAYER_DIR = DIR_RIGHT
PLAYER_TAIL = []
PLAYER_LENGTH = 0

APPLE_POINT = (-1, -1)

GAME_STATE = STATE_GAMEOVER
HIGHSCORE = 0

def puts(s):
    sys.stdout.write(s)

def display():
    for y in range(0, Y):
        for x in range(0, X):
            if (y, x) == PLAYER_POINT:
                puts('@')
            elif (y, x) in PLAYER_TAIL:
                puts('#')
            elif (y, x) == APPLE_POINT:
                puts('O')
            else:
                puts('.')
        puts('\n')

def move():
    global PLAYER_POINT, PLAYER_TAIL, GAME_STATE
    y, x = PLAYER_POINT
    
    PLAYER_TAIL.append((y, x))
    
    if PLAYER_DIR == DIR_UP:
        PLAYER_POINT = (y - 1, x)
    elif PLAYER_DIR == DIR_DOWN:
        PLAYER_POINT = (y + 1, x)
    elif PLAYER_DIR == DIR_LEFT:
        PLAYER_POINT = (y, x - 1)
    elif PLAYER_DIR == DIR_RIGHT:
        PLAYER_POINT = (y, x + 1)
    else:
        print("Unknown direction!")
        exit(1)
    
    if len(PLAYER_TAIL) > PLAYER_LENGTH:
        PLAYER_TAIL.pop(0)
     
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
    
    
   
def main():
    global PLAYER_DIR, PLAYER_POINT, GAME_STATE, APPLE_POINT, PLAYER_LENGTH, PLAYER_TAIL, HIGHSCORE

    while True:
        if GAME_STATE == STATE_GAMEOVER:
            puts("  PYTHON - SNAKE GAME  \n")
            puts(" [Q - Exit] [P - Play] ")
            
            if is_pressed('q'):
                puts(f"\033[{Y}B")
                if os.name != 'nt': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                exit()
            elif is_pressed('p'):
                if PLAYER_LENGTH > HIGHSCORE: HIGHSCORE = PLAYER_LENGTH
                PLAYER_POINT = (3, 5)
                PLAYER_DIR = DIR_RIGHT
                PLAYER_TAIL = []
                PLAYER_LENGTH = 0
                APPLE_POINT = (-1, -1)
                GAME_STATE = STATE_GAMELOOP
                sleep(1)
                
            puts("\033[1A\r")
        elif GAME_STATE == STATE_GAMELOOP:
            display()
            
            if is_pressed('w') and PLAYER_DIR != DIR_DOWN:
                PLAYER_DIR = DIR_UP
            elif is_pressed('s') and PLAYER_DIR != DIR_UP:
                PLAYER_DIR = DIR_DOWN
            elif is_pressed('a') and PLAYER_DIR != DIR_RIGHT:
                PLAYER_DIR = DIR_LEFT
            elif is_pressed('d') and PLAYER_DIR != DIR_LEFT:
                PLAYER_DIR = DIR_RIGHT
            
            if APPLE_POINT == (-1, -1):
                APPLE_POINT = PLAYER_POINT
                while APPLE_POINT == PLAYER_POINT or APPLE_POINT in PLAYER_TAIL:
                    APPLE_POINT = (randint(0, Y - 1), randint(0, X - 1))
             
            move()
            
            if PLAYER_POINT[0] > Y - 1 or PLAYER_POINT[1] > X - 1 or PLAYER_POINT[0] < 0 or PLAYER_POINT[1] < 0:
                GAME_STATE = STATE_GAMEOVER
            elif PLAYER_POINT in PLAYER_TAIL:
                GAME_STATE = STATE_GAMEOVER
            elif PLAYER_POINT == APPLE_POINT:
                PLAYER_LENGTH += 1
                APPLE_POINT = (-1, -1)
             
            puts(f"{'[NEW HIGHSCORE] ' if PLAYER_LENGTH > HIGHSCORE else ' '*16}[{PLAYER_LENGTH} POINTS]\n")
            puts(f"\033[{Y + 1}A\r")
        else:
            print("Unknown game state!")
            exit(1)
        
        sleep(0.08)
        
if __name__ == "__main__":
    main()
