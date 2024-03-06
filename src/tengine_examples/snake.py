from tengine import Point, key_pressed
import tengine
from enum import IntEnum
from random import randint

class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class GameState(IntEnum):
    MENU = 0
    GAME = 1

Game_State = GameState.MENU

Player: Point
Player_Direction: Direction
Player_Tail: list[Point]
Player_Length = 0

Highscore = 0

Apple: Point

def menu():
    global Game_State, Highscore

    tengine.__BG_SYMBOL = ' '

    if Player_Length - 1 > Highscore:
        Highscore = Player_Length - 1
    
    heighscore = [f"[ HIGHSCORE: {Highscore} ]"]
    logo = [
        "                           ",
        "    ____          __       ",
        "   / __/__  ___ _/ /_____  ",
        "  _\\ \/ _ \\/ _ `/  '_/ -_) ",
        " /___/_//_/\\_,_/_/\\_\\\\__/  ",
        "  Snake made using tengine ",
        "                           ",
        "   [P - Play]  [Q - Quit]  "
    ]

    if key_pressed('q'):
        tengine.quit()
    elif key_pressed('p'):
        setup()
        tengine.__BG_SYMBOL = '.'
        Game_State = GameState.GAME
        return

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
                int(tengine.Y_SIZE / 2) - (int(len(heighscore) / 2) + 4),
                int(tengine.X_SIZE / 2) - int(len(heighscore[0]) / 2)
            )
        )
    

def game():
    global Player, Player_Tail, Player_Direction, Player_Length, Apple, Game_State

    Player_Tail.append(Player.dup())
    
    if Player_Direction == Direction.UP:
        Player.y -= 1
    elif Player_Direction == Direction.DOWN:
        Player.y += 1
    elif Player_Direction == Direction.LEFT:
        Player.x -= 1
    elif Player_Direction == Direction.RIGHT:
        Player.x += 1
    else:
        print("Unknown direction!")
        tengine.quit(tengine.Status.ERROR)
    
    if len(Player_Tail) > Player_Length:
        Player_Tail.pop(0)

    if key_pressed('w') and Player_Direction != Direction.DOWN:
        Player_Direction = Direction.UP
    elif key_pressed('s') and Player_Direction != Direction.UP:
        Player_Direction = Direction.DOWN
    elif key_pressed('a') and Player_Direction != Direction.RIGHT:
        Player_Direction = Direction.LEFT
    elif key_pressed('d') and Player_Direction != Direction.LEFT:
        Player_Direction = Direction.RIGHT

    if Apple is None:
        Apple = Player.dup()
        while Apple == Player or Apple in Player_Tail:
            Apple = Point(randint(0, tengine.Y_SIZE - 1), randint(0, tengine.X_SIZE - 1))
    
    if Player.y > tengine.Y_SIZE - 1 or Player.x > tengine.X_SIZE - 1 or Player.y < 0 or Player.x < 0:
        Game_State = GameState.MENU
        tengine.sleep(0.5)
        return
    elif Player in Player_Tail:
        Game_State = GameState.MENU
        tengine.sleep(0.5)
        return
    elif Player == Apple:
        Player_Length += 1
        Apple = None

    tengine.RenderQueue.clear()

    score = [f"[ SCORE: {Player_Length - 1} ]"]
    tengine.Strings2RenderQueue(score, Point(1, int(tengine.X_SIZE / 2) - int(len(score[0]) / 2)))

    tengine.RenderQueue.add(Player, '\u001b[32m@\u001b[0m')
    for segment in Player_Tail:
        tengine.RenderQueue.add(segment, '\u001b[32;1mo\u001b[0m')
    
    if Apple is not None:
        tengine.RenderQueue.add(Apple, '\u001b[31;1m*\u001b[0m')

def setup():
    global Player, Player_Direction, Player_Tail
    global Player_Length, Apple, Game_State

    Player = Point(int(tengine.Y_SIZE / 2) , 1)
    Player_Direction = Direction.RIGHT
    Player_Tail = []
    Player_Length = 1

    Apple = None

    tengine.RenderQueue.clear()

def update():
    if Game_State == GameState.MENU:
        menu()
    elif Game_State == GameState.GAME:
        game()
    

if __name__ == '__main__':
    tengine.init(yx_size = (20, 42), setup = setup, update = update, tickdelay = 0.13, bg_symbol=' ')
    tengine.Gameloop()    