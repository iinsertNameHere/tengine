from tengine import Point, key_pressed
import tengine
from enum import IntEnum

class Velocity(Point):
    def __init__(self, y: int = 0, x: int = 0):
        super().__init__(y, x)

class Player:
    def __init__(self, origin_y: int, origin_x: int, max_speed: int, jump_strength: int):
        self.point = Point(origin_y, origin_x)
        self.velocity = Velocity(0, 0)
        self.body = []

        self.max_speed = max_speed
        self.jump_strength = jump_strength

        self.Update()
    
    def Update(self):
        if self.velocity.x > 0:
            if self.isBlockRight():
                Robot.velocity.x = -1
            self.point.x += 1 if self.velocity.x < int(self.max_speed / 2) else 2
            self.velocity.x -= 1 if self.velocity.x < int(self.max_speed / 2) else 2
        elif self.velocity.x < 0:
            if self.isBlockLeft():
                Robot.velocity.x = +1
            self.point.x -= 1 if self.velocity.x > 0 - int(self.max_speed / 2) else 2
            self.velocity.x += 1 if self.velocity.x > 0 - int(self.max_speed / 2) else 2
        
        if self.velocity.y > 0:
            self.point.y += 1
        elif self.velocity.y < 0:
            self.point.y -= 1
            self.velocity.y += 1

        self.t = [f"({self.velocity.y}, {self.velocity.x})"]

        self.body = [
            Point(self.point.y - 1, self.point.x),
            Point(self.point.y, self.point.x - 1),
            self.point.dup(),
            Point(self.point.y, self.point.x + 1),
            Point(self.point.y + 1, self.point.x),
        ]

        if not self.isOnGround():
            if self.velocity.y < 3:
                self.velocity.y += 1
        elif self.velocity.y > 0:
            self.velocity.y = 0

    def isOnGround(self) -> bool:
        ground_point = self.body[len(self.body) - 1].dup()
        ground_point.y += 1
        return tengine.RenderQueue.get(ground_point) == '#'
    
    def isBlockLeft(self) -> bool:
        p = self.body[len(self.body) - 1].dup()
        left_points = [Point(p.y - 1, p.x - 1), Point(p.y, p.x - 1), Point(p.y + 1, p.x - 1)]

        for lp in left_points:
            if tengine.RenderQueue.get(lp) == '#':
                return True
        return False
    
    def isBlockRight(self) -> bool:
        p = self.body[len(self.body) - 1].dup()
        right_points = [Point(p.y - 1, p.x + 1), Point(p.y, p.x + 1), Point(p.y + 1, p.x + 1)]

        for rp in right_points:
            if tengine.RenderQueue.get(rp) == '#':
                return True
        return False
            
    def QueueForRender(self):
        tengine.RenderQueue.add(self.body[0], "@")
        tengine.RenderQueue.add(self.body[1], "/")
        tengine.RenderQueue.add(self.body[2], "|")
        tengine.RenderQueue.add(self.body[3], "\\")
        tengine.RenderQueue.add(self.body[4], "O")

        tengine.Strings2RenderQueue(self.t, Point(0, 0))

    def AddSpeed_Right(self):
        if Robot.velocity.x > self.max_speed:
            Robot.velocity.x += 2
        else:
            Robot.velocity.x = self.max_speed
    
    def AddSpeed_Left(self):
        if Robot.velocity.x < self.max_speed * -1:
            Robot.velocity.x -= 2
        else:
            Robot.velocity.x = self.max_speed * -1
    
    def Jump(self):
        Robot.velocity.y -= self.jump_strength

class Camera:
    def __init__(self, map: list[str], start = 0):
        self.map = map
        self.x = start

    def QueueForRender(self):
        rawframe = []
        for line in self.map:
            frame_line = line[self.x:len(self.map[0])]
            if len(frame_line) > tengine.X_SIZE:
                frame_line = frame_line[0:tengine.X_SIZE]
            rawframe.append(frame_line)

        frame = []
        for line in rawframe:
            line = ''.join(ch*5 for ch in line)

            frame.append(" "*len(line))
            frame.append(line)

        for y in range(0, tengine.Y_SIZE):
            for x in range(0, tengine.X_SIZE):
                try: 
                    ch = frame[y][x]
                except:
                    print(x)
                    exit()
                if ch != ' ':
                    tengine.RenderQueue.add(Point(y, x), ch)

        tengine.Strings2RenderQueue([f"X: {self.x}"], Point(0, 10))

    def ScrollRight(self, by: int):
        if self.x < len(self.map[0]) - 20:
            self.x += by
            return True
        return False
    
    def ScrollLeft(self, by: int):
        if self.x > 0:
            self.x -= by
            return True
        return False

Robot: Player
Frame: Camera

def setup():
    global Robot, Frame
    Robot = Player(10, 8, 16, 10)

    map = [
        "# #                  "+"# #                "+"# # #              #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "#                   "+"                    "+"                   #",
        "####################"+"####################"+"####################"
    ]
    Frame = Camera(map, 0)

def update():
    global Robot, Frame

    if key_pressed('d') and Robot.velocity.y == 0:
        Robot.AddSpeed_Right()
    elif key_pressed('a') and Robot.velocity.y == 0:
        Robot.AddSpeed_Left()
    
    if key_pressed(tengine.KEY_SPACE) and Robot.velocity.y == 0:
        Robot.Jump()
    
    ground_point = Robot.body[len(Robot.body) - 1].dup()
    ground_point.y += 1
    if tengine.RenderQueue.get(ground_point) != '#':
        if Robot.velocity.y < 3:
            Robot.velocity.y += 1
    elif Robot.velocity.y > 0:
        Robot.velocity.y = 0
    
    if (tengine.X_SIZE - 20) - Robot.point.x <= 0:
        if Frame.ScrollRight(1):
            Robot.point.x -= 1 if Robot.velocity.x < int(Robot.max_speed / 2) else 2
    elif 20 - Robot.point.x >= 0:
        if Frame.ScrollLeft(1):
            Robot.point.x += 1 if Robot.velocity.x > 0 - int(Robot.max_speed / 2) else 2

    Robot.Update()

    tengine.RenderQueue.clear()
    Robot.QueueForRender()
    Frame.QueueForRender()

if __name__ == '__main__':
    tengine.init(yx_size = (20, 100), setup = setup, update = update, tickdelay = 0.08, bg_symbol=' ')
    tengine.Gameloop()   