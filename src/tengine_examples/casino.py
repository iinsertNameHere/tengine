from tengine import Point, key_pressed
import tengine
import random
from enum import IntEnum
from time import sleep

class GameState(IntEnum):
    START = 0
    ROLLING = 1
    CHEKCING = 2
    LOCKED = 3

class Object:
    def __init__(self, lines: list[list[str]], dividend = 0):
        self.lines = lines
        self.dividend = dividend

    def win_margin(self, bet: int) -> int:
        if self.dividend == 0: return 0
        return bet / self.dividend

class Slot:
    def __init__(self, objs: list[Object], origin: Point, speed: int, border: int = tengine.Y_SIZE):
        self.speed: int = speed
        self.origin: Point = origin
        self.rounds: int = 0
        self.active_obj = None
        self.objects = objs
        self.border = border

    def chooseObj(self):
        self.active_obj = random.choice(self.objects)

    def draw(self):
        lines2d = [list(l) for l in self.active_obj.lines]
        origins = (self.origin, Point(self.origin.y + len(lines2d), self.origin.x + len(lines2d[0])))
        idxs = []
        points = []

        for y in range(0, origins[1].y - origins[0].y):
            for x in range(0, origins[1].x - origins[0].x):
                idxs.append(Point(y, x))

        for y in range(origins[0].y, origins[1].y):
            for x in range(origins[0].x, origins[1].x):
                points.append(Point(y, x))
        
        for i, point in enumerate(points):
            if point.y >= self.border:
                continue
            
            idx = idxs[i]
            ch = lines2d[idx.y][idx.x]
            tengine.RenderQueue.add(point, ch)

class Wallet:
    def __init__(self, balance: int):
        self.balance = balance
        self.last_action = '='
        self.bet = 1

    def withdraw(self, amount: int):
        self.balance -= amount
        self.last_action = f'- {amount}'
    
    def add(self, amount: int):
        self.balance += amount
        self.last_action = f'+ {amount}'

    def add_bet(self, amount: int):
        self.bet += amount
        if self.bet > self.balance:
            self.bet = self.balance
    
    def remove_bet(self, amount: int):
        self.bet -= amount
        if self.bet < 1:
            self.bet = 1


OBJ_DIAMOND = Object([
" ______ ",
"/_|__|_\\",
"'.\  /.'",
" '.\/.' ",
"   ''   "
], dividend = 3)

OBJ_BOWL = Object([ 
" , \\  ",
"()/°\\(_",
"\\:::::/",
" \\:::/ "
], dividend = 4)

OBJ_BANANA = Object([ 
" _ \'-_,# ",
"_\'--','`|",
"\`---`  / ",
" `----'`  "
], dividend = 5)

OBJ_PINEAPPLE = Object([
" \\|/ ",
" AXA ",
"/XXX\\",
"\\XXX/",
" `^' "
])

OBJ_GRAPES = Object([
"  \\   ",
" ()() ",
"()()()",
" ()() ",
"  ()  "
])

OBJ_APPLE = Object([
"  ,-/,. ",
" / #   \\",
"|      |",
" `_,._,'"
])

SLOT1: Slot
SLOT2: Slot
SLOT3: Slot
OBJS = [OBJ_DIAMOND, OBJ_BOWL, OBJ_BANANA, OBJ_PINEAPPLE, OBJ_PINEAPPLE, OBJ_PINEAPPLE, OBJ_GRAPES, OBJ_GRAPES, OBJ_APPLE, OBJ_APPLE]

ROUNDS = 5
STATE: GameState = GameState.START
ON = True

BALANCE = Wallet(100)

def Draw(DRAW_SLOTS = False, DRAW_BOX = True):

    if DRAW_BOX:
        for y in range(0, 10):
            tengine.RenderQueue.add(Point(y, 24), "|")

        for y in range(0, 10):
            tengine.RenderQueue.add(Point(y, 48), "|")

    for x in range(0, 72):
            tengine.RenderQueue.add(Point(10, x), "-")

    tengine.Strings2RenderQueue([str(BALANCE.balance)], Point(11, 1))
    tengine.Strings2RenderQueue([str(BALANCE.bet)], Point(11, int((72 / 2) - (len(str(BALANCE.bet)) / 2))))
    tengine.Strings2RenderQueue([str(BALANCE.last_action)], Point(11, 71 - len(BALANCE.last_action)))

    if DRAW_SLOTS:
        SLOT1.draw()
        SLOT2.draw()
        SLOT3.draw()

def randpop(l: list):
    idx = random.randint(0, len(l) - 1)
    e = l.pop(idx)
    return (l, e)

def setup():
    global SLOT1, SLOT2, SLOT3, STATE, ON, BALANCE
    
    speeds = [6, 5, 7]
    speeds, SLOT1_SPEED = randpop(speeds)
    speeds, SLOT2_SPEED = randpop(speeds)
    speeds, SLOT3_SPEED = randpop(speeds)

    SLOT1 = Slot(OBJS, Point(-5, 9), SLOT1_SPEED, 10)
    SLOT2 = Slot(OBJS, Point(-5, 33), SLOT2_SPEED, 10)
    SLOT3 = Slot(OBJS, Point(-5, 57), SLOT3_SPEED, 10)

    SLOT1.chooseObj()
    SLOT2.chooseObj()
    SLOT3.chooseObj()

    STATE = GameState.START
    ON = True

def update():
    global STATE, SLOT1, SLOT2, SLOT3, ON, BALANCE

    if BALANCE.bet > BALANCE.balance:
        BALANCE.bet = BALANCE.balance

    if BALANCE.balance <= 0:
        print("Game over!")
        tengine.quit()

    if (STATE == GameState.START):
        if (key_pressed('+')): BALANCE.add_bet(1)
        if (key_pressed('-')): BALANCE.remove_bet(1)

        if (key_pressed(tengine.KEY_SPACE)): STATE = GameState.ROLLING

        tengine.RenderQueue.clear()
        Draw(DRAW_BOX = False)
        tengine.Strings2RenderQueue([
            "   ___          _             ",            
            "  / __\__ _ ___(_)_ __   ___  ",
            " / /  / _` / __| | '_ \ / _ \ ",
            "/ /__| (_| \__ \ | | | | (_) |",
            "\____/\__,_|___/_|_| |_|\___/ "
        ], Point(3, 21))

    elif (STATE == GameState.ROLLING):
        tengine.RenderQueue.clear()

        if (SLOT1.origin.y >= 10):
            SLOT1.chooseObj()
            SLOT1.origin.y = -5
            SLOT1.rounds += 1
        if (SLOT2.origin.y >= 10):
            SLOT2.chooseObj()
            SLOT2.origin.y = -5
            SLOT2.rounds += 1
        if (SLOT3.origin.y >= 10):
            SLOT3.chooseObj()
            SLOT3.origin.y = -5
            SLOT3.rounds += 1

        if (SLOT1.rounds >= ROUNDS):
            SLOT1.rounds = 0
            SLOT1.speed -= 1
        if (SLOT2.rounds >= ROUNDS):
            SLOT2.rounds = 0
            SLOT2.speed -= 1
        if (SLOT3.rounds >= ROUNDS):
            SLOT3.rounds = 0
            SLOT3.speed -= 1

        if (SLOT1.speed <= 0):
            if (SLOT1.origin.y < 3): SLOT1.origin.y += 1
        if (SLOT2.speed <= 0):
            if (SLOT2.origin.y < 3): SLOT2.origin.y += 1
        if (SLOT3.speed <= 0):
            if (SLOT3.origin.y < 3): SLOT3.origin.y += 1

        SLOT1.origin.y += SLOT1.speed
        SLOT2.origin.y += SLOT2.speed
        SLOT3.origin.y += SLOT3.speed

        Draw(True)

        if (SLOT1.speed <= 0 and SLOT1.origin.y == 3 and
            SLOT2.speed <= 0 and SLOT2.origin.y == 3 and
            SLOT3.speed <= 0 and SLOT3.origin.y == 3):
                STATE = GameState.CHEKCING
    elif (STATE == GameState.CHEKCING):
        tengine.RenderQueue.clear()

        Draw(ON)

        if (not ON):
            SLOT1.rounds += 1
            SLOT2.rounds += 1
            SLOT3.rounds += 1

        ON = (not ON)
        
        if (SLOT1.rounds == 5 and SLOT2.rounds == 5 and SLOT3.rounds == 5):
            tengine.__TICKDELAY = 0.1
            win1 = SLOT1.active_obj.win_margin(BALANCE.bet)
            win2 = SLOT2.active_obj.win_margin(BALANCE.bet)
            win3 = SLOT3.active_obj.win_margin(BALANCE.bet)
            win = win1 + win2 + win3

            if int(win) <= 0:
                BALANCE.withdraw(BALANCE.bet)
            else:
                BALANCE.add(int(win))

            tengine.RenderQueue.clear()
            Draw(True)
            for x in range(0, 72):
                tengine.RenderQueue.add(Point(3, x), "-")
                tengine.RenderQueue.add(Point(4, x), " ")
                tengine.RenderQueue.add(Point(5, x), "-")

                tengine.Strings2RenderQueue(["+ " + str(int(win1)) if win1 > 0 else "--"], Point(4, 11))
                tengine.Strings2RenderQueue(["+ " + str(int(win2)) if win2 > 0 else "--"], Point(4, 35))
                tengine.Strings2RenderQueue(["+ " + str(int(win3)) if win3 > 0 else "--"], Point(4, 59))

            tengine.Flush()
            tengine.Display()

            sleep(4)

            setup()         

if __name__ == "__main__":
    tengine.init(yx_size=(12, 72), setup = setup, update = update, tickdelay=0.1, bg_symbol=' ')
    tengine.Gameloop()
