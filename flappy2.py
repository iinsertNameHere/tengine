from tengine import Point, puts, key_pressed, STATUS_ERROR
import tengine
from random import randint

PLAYER: Point
PLAYER_VELOCITY = 0
PLAYER_BODY: list[Point] = []

def BUILD_PLAYER():
    return [
        PLAYER - Point(1, 0),
        PLAYER,
        PLAYER + Point(0, 1),
        PLAYER + Point(1, 0)
    ]

PIPES: list[tuple[Point, Point]] = []
PIPE_BODYS: list[Point] = []

def BUILD_PIPES():
    bodys = []
    
    for pipe_pair in PIPES:
    
        # Build TOP Pipe
        for y in range(0, pipe_pair[0].y + 1):
            bodys += [
                Point(y, pipe_pair[0].x - 2),
                Point(y, pipe_pair[0].x - 1),
                Point(y, pipe_pair[0].x),
                Point(y, pipe_pair[0].x + 1),
                Point(y, pipe_pair[0].x + 2)
            ]
        
        # Build BOTTOM Pipe
        for y in range(pipe_pair[1].y, tengine.Y_SIZE):
            bodys += [
                Point(y, pipe_pair[1].x - 2),
                Point(y, pipe_pair[1].x - 1),
                Point(y, pipe_pair[1].x),
                Point(y, pipe_pair[1].x + 1),
                Point(y, pipe_pair[1].x + 2)
            ]
            
    return bodys

SPAWN_DELAY = 0
def SPAWN_PIPE():
    global PIPES
    
    x = tengine.X_SIZE + 3
    y = randint(3, 20)
    
    PIPES.append((Point(y, x), Point(y + 10, x)))

GS_MENU = 0
GS_GAME = 1

GAMESTATE: int

def setup():
    global GAMESTATE, PLAYER, PLAYER_VELOCITY, PLAYER_BODY, PIPES, PIPE_BODYS, SPAWN_DELAY
    
    # Init Game State
    GAMESTATE = GS_MENU
    
    # Init Player
    PLAYER = Point(10, 15)
    PLAYER_VELOCITY = 0
    PLAYER_BODY = BUILD_PLAYER()
    
    # Init Pipes
    PIPES = []
    PIPE_BODYS = []
    
    # Init Spawn Delay
    SPAWN_DELAY = 0

def menu():
    logo = "" \
    + "  _____ _                    _____ _       _  \n" \
    + " |   __| |___ ___ ___ _ _   | __  |_|___ _| | \n" \
    + " |   __| | .'| . | . | | |  | __ -| |  _| . | \n" \
    + " |__|  |_|__,|  _|  _|_  |  |_____|_|_| |___| \n" \
    + "             |_| |_| |___|                     "

    logo_rect = [(0, 0), (len(logo.split('\n')[0]), len(logo.split('\n')))]
    y_coords = [y for y in range(logo_rect[0][1], logo_rect[1][1] + 1)]
    x_coords = [x for x in range(logo_rect[0][0], logo_rect[1][0] + 1)]
    logo_points = [Point(y, x) for x in x_coords for y in y_coords]
    
    logo2d = [ list(s) for s in logo.split('\n')]
    for p in logo_points:
        print(p)
        print(logo2d[p.y][p.x])
        tengine.Add_RenderPoint(p, logo2d[p.y][p.x])
        
    tengine.Clear_RenderPoints()
    
def game():
    global PLAYER_VELOCITY, PLAYER_BODY, PLAYER, SPAWN_DELAY, PIPE_BODYS, PIPES, GAMESTATE
    
    # Checking for Gameover
    if PLAYER.y <= 0 or PLAYER.y >= tengine.Y_SIZE - 1:
        GAMESTATE = GS_MENU
        return
    
    for p in PLAYER_BODY:
        if p in PIPE_BODYS:
            GAMESTATE = GS_MENU
            return
    
    # Graity Handling
    if PLAYER_VELOCITY > 0:
        if PLAYER_VELOCITY > 2:
            PLAYER_VELOCITY = 2
        PLAYER_VELOCITY -= 1
        PLAYER.y -= 1
    elif PLAYER_VELOCITY < 1:
        PLAYER_VELOCITY -= 1
        PLAYER.y += 2
    else:
        print("Invalid PLAYER_VELOCITY!")
        tengine.quit(STATUS_ERROR)
    
    # Handling pipe Spawning
    if SPAWN_DELAY <= 0:
        SPAWN_DELAY = 30
        SPAWN_PIPE()
        
    # Moving Pipes
    newpipes = []
    for pipe_pair in PIPES:
        pipe1, pipe2 = pipe_pair
        
        pipe1 = Point(pipe1.y, pipe1.x - 1)
        pipe2 = Point(pipe2.y, pipe2.x - 1)
        
        if pipe1.x + 1 >= 0:
            newpipes.append((pipe1, pipe2))
    
    PIPES = newpipes
    
    # Keypress Handling
    if key_pressed('f'):
        if PLAYER_VELOCITY <= 0:
            PLAYER_VELOCITY = 2
        else:
            PLAYER_VELOCITY += 1
    
    # Prep for next Tick
    tengine.Clear_RenderPoints()
    
    PIPE_BODYS = BUILD_PIPES()
    for p in PIPE_BODYS:
        tengine.Add_RenderPoint(p, '#')
    
    PLAYER_BODY = BUILD_PLAYER()
    for p in PLAYER_BODY:
        tengine.Add_RenderPoint(p, 'O')
        
    SPAWN_DELAY -= 1

def update():
    if GAMESTATE == GS_MENU:
        menu()
    elif GAMESTATE == GS_GAME:
        game()
        
    
if __name__ == '__main__':
    tengine.init(yx_size = (30, 70), setup = setup,update = update, tickdelay = 0.1)
    tengine.Gameloop()    