from tengine import Point, puts, key_pressed, STATUS_ERROR
import tengine
from random import randint

Player: Point
Player_Velocity = 0
Player_Body: list[Point] = []

def BUILD_PLAYER():
    return [
        Player - Point(1, 0),
        Player,
        Player + Point(0, 1),
        Player + Point(1, 0)
    ]

Pipes: list[tuple[Point, Point]] = []
Pipe_Bodys: list[Point] = []

def BUILD_PIPES():
    bodys = []
    
    for pipe_pair in Pipes:
    
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

Spawn_Delay = 0
def SPAWN_PIPE():
    global Pipes
    
    x = tengine.X_SIZE + 3
    y = randint(3, 20)
    
    Pipes.append((Point(y, x), Point(y + 10, x)))

GS_MENU = 0
GS_GAME = 1

Game_State: int

Score = 0
Highscore = 0

def setup():
    global Game_State, Player, Player_Velocity, Player_Body
    global Pipes, Pipe_Bodys, Spawn_Delay, Score
    
    # Init Game State
    Game_State = GS_MENU
    
    # Init Player
    Player = Point(10, 15)
    Player_Velocity = 0
    Player_Body = BUILD_PLAYER()
    
    # Init Pipes
    Pipes = []
    Pipe_Bodys = []
    
    # Init Spawn Delay
    Spawn_Delay = 0

    Score = 0

def menu():
    global Game_State, Score, Highscore

    if Score > Highscore:
        Highscore = Score
    
    heighscore = [f"[ HIGHSCORE: {Highscore} ]"]
    logo = [
        "                                              ",
        "  _____ _                    _____ _       _  ",
        " |   __| |___ ___ ___ _ _   | __  |_|___ _| | ",
        " |   __| | .'| . | . | | |  | __ -| |  _| . | ",
        " |__|  |_|__,|  _|  _|_  |  |_____|_|_| |___| ",
        "             |_| |_| |___|                    ",
        "   FlappyBird mady by iinsert using tengine   ",
        "                                              ",
        "                                              ",
        "            [P - Play]   [Q - Quit]           "
    ]

    if key_pressed('q'):
        tengine.quit()
    elif key_pressed('p'):
        setup()
        Game_State = GS_GAME

    tengine.RenderQueue.clear()
    tengine.Strings2RenderQueue(
        logo,
        Point(
            int(tengine.Y_SIZE / 2) - int(len(logo) / 2),
            int(tengine.X_SIZE / 2) - int(len(logo[0]) / 2)
        )
    )
    if Highscore > 0:
        tengine.Strings2RenderQueue(
            heighscore,
            Point(
                int(tengine.Y_SIZE / 2) - (int(len(heighscore) / 2) + 5),
                int(tengine.X_SIZE / 2) - int(len(heighscore[0]) / 2)
            )
        )

def game():
    global Player_Velocity, Player_Body, Player, Spawn_Delay
    global Pipe_Bodys, Pipes, Game_State, Score
    
    # Checking for Gameover
    if Player.y <= 0 or Player.y >= tengine.Y_SIZE - 1:
        Game_State = GS_MENU
        return
    
    for p in Player_Body:
        if p in Pipe_Bodys:
            Game_State = GS_MENU
            return
    
    # Graity Handling
    if Player_Velocity > 0:
        Player_Velocity -= 1
        Player.y -= 1
    elif Player_Velocity < 1:
        Player_Velocity -= 1
        Player.y += 2
    else:
        print("Invalid Player Velocity!")
        tengine.quit(STATUS_ERROR)
    
    # Handling pipe Spawning
    if Spawn_Delay <= 0:
        Spawn_Delay = 30
        SPAWN_PIPE()
        
    # Moving Pipes
    newpipes = []
    for pipe_pair in Pipes:
        pipe1, pipe2 = pipe_pair
        
        pipe1 = Point(pipe1.y, pipe1.x - 1)
        pipe2 = Point(pipe2.y, pipe2.x - 1)
        
        if pipe1.x + 1 >= 0:
            newpipes.append((pipe1, pipe2))
    
    Pipes = newpipes
    
    # Keypress Handling
    if key_pressed(tengine.KEY_SPACE):
        if Player_Velocity <= 0:
                Player_Velocity = 2
        elif Player_Velocity > 0:
            if Player_Velocity > 10:
                Player_Velocity = 10
            else:
                Player_Velocity += 2
    
    # Prep for next Tick
    tengine.RenderQueue.clear()
    
    Pipe_Bodys = BUILD_PIPES()
    for p in Pipe_Bodys:
        tengine.RenderQueue.add(p, '#')
    
    Player_Body = BUILD_PLAYER()
    for p in Player_Body:
        tengine.RenderQueue.add(p, 'O')

    for pipe_pair in Pipes:
        if pipe_pair[0].x + 3 == Player.x:
            Score += 1

    score = [f"[ SCORE: {Score} ]"]
    tengine.Strings2RenderQueue(
        score,
        Point(1, int(tengine.X_SIZE / 2) - int(len(score[0]) / 2))
    )

    Spawn_Delay -= 1

def update():
    if Game_State == GS_MENU:
        menu()
    elif Game_State == GS_GAME:
        game()
        
    
if __name__ == '__main__':
    tengine.init(yx_size = (30, 70), setup = setup, update = update, tickdelay = 0.1)
    tengine.Gameloop()    