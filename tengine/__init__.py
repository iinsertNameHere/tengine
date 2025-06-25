import sys
import os
from time import sleep
from enum import IntEnum
from .color import Color, fgcolor, bgcolor, frmt, len_no_ansi, split_and_group_ansi

if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios

class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.y = y
        self.x = x
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __add__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return Point(self.x + p.x, self.y + p.y)
    
    def __iadd__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        self.x += p.x
        self.y += p.y
        return self
        
    def __radd__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return self.__add__(p)
        
    def __sub__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return Point(self.x - p.x, self.y - p.y)
    
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
        return (self.x, self.y) == (p.x, p.y)
    
    def __ne__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) != (p.x, p.y)
    
    def __gt__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) > (p.x, p.y)
    
    def __lt__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) < (p.x, p.y)
    
    def __ge__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) > (p.x, p.y)
    
    def __le__(self, p):
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) < (p.x, p.y)
    
    def dup(self):
        """
            Returns a duplicate of itself
        """
        return Point(self.x, self.y)

class RenderQueue:
    def __init__(self, queue: dict = {}):
        self.__queue: dict[tuple[int, int]] = queue

    def __repr__(self) -> str:
        return str(self.__queue)
    
    def __str__(self) -> str:
        return str(self.__queue)

    def __add__(self, rq):
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        return RenderQueue(self.__queue + rq.asDict())

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
        return [Point(p.x, p.y) for p in self.__queue.keys()]
    
    def get(self, point) -> str|None:
        return self.__queue.get((point.x, point.y))
    
    def add_point(self, point: Point, symbol: str):
        self.__queue[(point.x, point.y)] = symbol

    def add_string(self, string: str, origin: Point):
        lines = string.split("\n")
        lines2d = [split_and_group_ansi(l.replace("\n", "")) for l in lines]
        origins = (origin, Point(origin.x + len(lines2d[0]), origin.y + len(lines2d)))
        idxs = []
        points = []

        for y in range(0, origins[1].y - origins[0].y):
            for x in range(0, origins[1].x - origins[0].x):
                idxs.append(Point(x, y))

        for y in range(origins[0].y, origins[1].y):
            for x in range(origins[0].x, origins[1].x):
                points.append(Point(x, y))
        
        for i, point in enumerate(points):
            idx = idxs[i]
            ch = lines2d[idx.y][idx.x]
            self.add_point(point, ch)

    def clear(self):
        self.__queue = {}

class RenderManager:
    def __init__(self, x_size, y_size, border):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__border = border
        self.__lines = 0
    
    def puts(self, s: str, overwrite: bool = True):
        if '\n' in s and overwrite:
            self.__lines += 1
        sys.stdout.write(s)

    def display(self, render_queue: RenderQueue, bg_symbol: str):
        if self.__border: self.puts(f"." + ("-"*self.__x_size) + '.\n')
        for y in range(0, self.__y_size):
            if self.__border: self.puts('|')
            for x in range(0, self.__x_size):
                symbol = render_queue.get(Point(x, y))
                if symbol:
                    if '\0' in symbol:
                        symbol = symbol.replace('\0', bg_symbol)
                    self.puts(symbol)
                else:
                    self.puts(bg_symbol)
            if self.__border: self.puts('|')
            self.puts('\n')
        if self.__border: self.puts("`" + ("-"*self.__x_size) + '´\n')

    def flush(self):
        self.puts(f"\033[{self.__lines}A\r")
        self.__lines = 0
    


def handler_function(key):
    pass
handler_func = type(handler_function)

class InputManager:
    def __init__(self):
        self.input_blocked: bool = False
        self.__key = None
        self.__bindings: dict[chr, func] = {}
        self.__blocked_keys: list[chr] = []

    def __key_pressed(self, key: str) -> bool:
        if os.name == 'nt':
            if msvcrt.kbhit():
                try:
                    self.__key = msvcrt.getch().decode('utf-8')
                except:
                    self.__key = None
        else:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                self.__key = sys.stdin.read(1)

        if self.__key == key and key not in self.__blocked_keys:
            self.__key = None
            return True
        return False

    def add_binding(self, key: chr, handler: handler_func):
        if self.__bindings.get(key):
            raise ValueError(f"Binding for key '{key}' already exists!")
        self.__bindings[key] = handler

    def block_key(self, key):
        if key not in self.__blocked_keys:
            self.__blocked_keys.append(key)
    
    def allow_key(self, key):
        if key in self.__blocked_keys:
            self.__blocked_keys.remove(key)

    def update(self):
        for key in self.__bindings.keys():
            if self.__key_pressed(key): self.__bindings[key](key)


class Scene:
    def __init__(self, tickdelay: float = 0.08, bg_symbol: chr = ' '):
        self.tickdelay: float = tickdelay
        self.bg_symbol: chr = bg_symbol
        self.render_queue = RenderQueue()
        self.input_manager = InputManager()

    def setup(self):
        pass

    def update(self):
        pass


class Game:
    def __init__(self, x_size: int, y_size: int, border: bool = True):
        os.system("") # Prep terminal for formating codes

        if os.name != 'nt':
            self.__old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

        self.__quit_status: int = ""
        self.__scenes: dict[str, Scene] = {}
        self.__active_scene: str = None
        self.x_size = x_size
        self.y_size = y_size

        self.render_manager = RenderManager(x_size, y_size, border)

    def cleanup(self):
        if os.name != 'nt':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__old_settings)

    def quit(self, status: int = None):
        if status == None:
            status = self.__quit_status
        self.cleanup()
        exit(status)

    def add_scene(self, name: str, scene: Scene):
        if self.__scenes.get(name):
            raise ValueError(f'A Scene with the name "{name}" already exists!')

        self.__scenes[name] = scene
    
    def set_scene(self, name: str):
        if not self.__scenes.get(name):
            raise ValueError(f'A Scene with the name "{name}" dose not exists! Add scenes by using the Geme.add_scene function.')

        self.__active_scene = name

    def run(self):
        if not self.__active_scene:
            raise RuntimeError("No active Scene was set! Please use Game.set_scene to do so.")
        
        prev_scene = self.__active_scene
        scene = self.__scenes[self.__active_scene]
        while True:
            if prev_scene != self.__active_scene:
                scene = self.__scenes[self.__active_scene]
                prev_scene = self.__active_scene

                scene.render_queue.clear()
                scene.setup()

            self.render_manager.display(scene.render_queue, scene.bg_symbol)

            scene.render_queue.clear()
            scene.update()
            scene.input_manager.update()

            self.render_manager.flush()
            sleep(scene.tickdelay)