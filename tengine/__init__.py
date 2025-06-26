import sys
import os
from time import sleep
from enum import IntEnum
from .color import Color, fgcolor, bgcolor, frmt, len_no_ansi, split_and_group_ansi
import math
from collections import defaultdict

if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios

class Point:
    pass

class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.y = y
        self.x = x
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __add__(self, p: Point) -> Point:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return Point(self.x + p.x, self.y + p.y)
    
    def __iadd__(self, p: Point) -> Point:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        self.x += p.x
        self.y += p.y
        return self
        
    def __radd__(self, p: Point) -> Point:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return self.__add__(p)
        
    def __sub__(self, p: Point) -> Point:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return Point(self.x - p.x, self.y - p.y)
    
    def __isub__(self, p: Point) -> Point:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        self.y -= p.y
        self.x -= p.x
        return self
        
    def __rsub__(self, p: Point) -> Point:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return self.__sub__(p)
        
    def __eq__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) == (p.x, p.y)
    
    def __ne__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) != (p.x, p.y)
    
    def __gt__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) > (p.x, p.y)
    
    def __lt__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) < (p.x, p.y)
    
    def __ge__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) > (p.x, p.y)
    
    def __le__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) < (p.x, p.y)

    def dup(self):
        """ Returns a duplicate of this point """
        return Point(self.x, self.y) 

class RenderQueue:
    pass

class RenderQueue:
    def __init__(self, queue: dict[tuple[int, int], str] = {}):
        self.__queue: dict[tuple[int, int], str] = queue

    def __repr__(self) -> str:
        return str(self.__queue)
    
    def __str__(self) -> str:
        return str(self.__queue)

    def __add__(self, rq: RenderQueue) -> RenderQueue:
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        d = {}
        d.update(self.__queue)
        d.update(rg.asDict())
        return RenderQueue(d)

    def __iadd__(self, rq: RenderQueue) -> RenderQueue:
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        self.__queue.update(rq.asDict())
        return self
        
    def __radd__(self, rq: RenderQueue) -> RenderQueue:
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        return self.__add__(rq)
    
    def asDict(self) -> dict[tuple[int, int], str]:
        return self.__queue

    def points(self) -> list[Point]:
        return [Point(p.x, p.y) for p in self.__queue.keys()]
    
    def get(self, point) -> str|None:
        return self.__queue.get((point.x, point.y))
    
    def add_point(self, point: Point, symbol: str) -> None:
        self.__queue[(point.x, point.y)] = symbol

    def add_string(self, string: str, origin: Point) -> None:
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

    def add_line(self, point0: Point, point1: Point, symbol: str) -> list[Point]:
        x0 = point0.x
        y0 = point0.y
        x1 = point1.x
        y1 = point1.y

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        points = []
        while True:
            points.append(Point(x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        
        for p in points:
            self.add_point(p, symbol)

        return points

    def add_circle(self, origin: Point, radius: int, symbol: str, filled=False, cell_width=2, cell_height=1) -> list[Point]:
        xc = origin.x
        yc = origin.y
        r = radius

        points = []
        aspect_ratio = cell_width / cell_height
        r_scaled_x = r * aspect_ratio  # Scale radius for X-axis
        
        # First get all boundary points
        for angle in range(0, 360, 1):  # 1-degree steps for smoothness
            rad = math.radians(angle)
            x = round(xc + r_scaled_x * math.cos(rad))
            y = round(yc + r * math.sin(rad))
            points.append(Point(x, y))
        
        if filled:
            # Get min/max y to scan vertically
            min_y = yc - r
            max_y = yc + r
            
            for y in range(min_y, max_y + 1):
                # Calculate left/right boundaries at this y level
                y_rel = y - yc
                if abs(y_rel) > r:
                    continue
                    
                # Calculate x bounds (scaled by aspect ratio)
                x_width = math.sqrt(r**2 - y_rel**2) * aspect_ratio
                x_start = round(xc - x_width)
                x_end = round(xc + x_width)
                
                # Add all horizontal points between boundaries
                for x in range(x_start, x_end + 1):
                    points.append(Point(x, y))
        

        for p in points:
            self.add_point(p, symbol)
        
        return points

    def add_rectangle(self, top_left: Point, width: int, height: int, symbol: str, filled=False) -> list[Point]:
        """Draw a rectangle with optional fill."""
        points = []
        x1, y1 = top_left.x, top_left.y
        x2, y2 = x1 + width - 1, y1 + height - 1

        if filled:
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    points.append(Point(x, y))
        else:
            # Draw four sides
            for x in range(x1, x2 + 1):
                points.append(Point(x, y1))  # Top
                points.append(Point(x, y2))  # Bottom
            for y in range(y1 + 1, y2):
                points.append(Point(x1, y))  # Left
                points.append(Point(x2, y))  # Right

        for p in points:
            self.add_point(p, symbol)
        return points

    def add_triangle(self, p1: Point, p2: Point, p3: Point, symbol: str, filled=False) -> list[Point]:
        """Draw a triangle with optional fill."""
        points = []
        
        def sign(a: Point, b: Point, c: Point) -> float:
            return (a.x - c.x) * (b.y - c.y) - (b.x - c.x) * (a.y - c.y)

        # Find bounding box
        min_x = min(p1.x, p2.x, p3.x)
        max_x = max(p1.x, p2.x, p3.x)
        min_y = min(p1.y, p2.y, p3.y)
        max_y = max(p1.y, p2.y, p3.y)

        if filled:
            # Barycentric coordinate method for fill
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    p = Point(x, y)
                    d1 = sign(p, p1, p2)
                    d2 = sign(p, p2, p3)
                    d3 = sign(p, p3, p1)

                    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
                    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

                    if not (has_neg and has_pos):
                        points.append(p)
        else:
            # Draw three edges
            points.extend(self.add_line(p1, p2, symbol))
            points.extend(self.add_line(p2, p3, symbol))
            points.extend(self.add_line(p3, p1, symbol))

        for p in points:
            self.add_point(p, symbol)
        return points

    def clear(self) -> None:
        self.__queue = {}

class Sprite:
    def __init__(self, pixels: list, width: int, height: int, transparent_color: tuple = (0, 0, 0)):
        self.pixels = pixels
        self.width = width
        self.height = height
        self.transparent_color = transparent_color
    
    def flip(self, horizontal: bool, vertical: bool):
        """Flip sprite along axes"""
        new_pixels = []
        for y in range(self.height):
            new_y = self.height - 1 - y if vertical else y
            row = []
            for x in range(self.width):
                new_x = self.width - 1 - x if horizontal else x
                row.append(self.pixels[new_y][new_x])
            new_pixels.append(row)
        self.pixels = new_pixels
        return self

    def dup(self):
        return Sprite(self.pixels, self.width, self.height, self.transparent_color)

class SpriteManager:
    def __init__(self):
        self.sprites = {}
    
    def load_sprite(self, name: str, filepath: str, transparent_color: tuple = (0, 0, 0)) -> Sprite:
        """Load PPM file into sprite storage with optional transparency"""
        pixels, width, height = self._load_ppm(filepath)
        # Ensure even height for proper half-block pairing
        if height % 2 != 0:
            height -= 1
            pixels = pixels[:height]
        self.sprites[name] = Sprite(pixels, width, height, transparent_color)
        return self.sprites[name]
    
    def render_sprite(
        self,
        rq: RenderQueue,
        sprite_name: str,
        origin: Point,
        center_origin: bool = False,
        flip_h: bool = False,
        flip_v: bool = False,
        bg_symbol_fmrt: str = ''
    ) -> list[Point]:
        """Render sprite to render queue using half-block characters with transparency"""
        sprite = self.sprites[sprite_name]
        
        # Create flipped copy if needed
        sprite_copy = sprite.dup().flip(flip_h, flip_v)
        
        # Calculate offsets if centering
        x_offset = -sprite_copy.width // 2 if center_origin else 0
        y_offset = -sprite_copy.height // 4 if center_origin else 0  # Divided by 4 because we're combining 2 rows
        
        points = []

        # Process pixels in vertical pairs
        for y in range(0, sprite_copy.height - 1, 2):
            for x in range(sprite_copy.width):
                # Get top and bottom pixels
                top_pixel = sprite_copy.pixels[y][x]
                bottom_pixel = sprite_copy.pixels[y+1][x] if y+1 < sprite_copy.height else sprite_copy.transparent_color
                
                # Skip if both pixels are transparent
                if (top_pixel == sprite_copy.transparent_color and 
                    bottom_pixel == sprite_copy.transparent_color):
                    continue
                
                # Create colored half-block character
                if top_pixel == sprite_copy.transparent_color:
                    # Only bottom pixel has color - use lower half block
                    char = f"{Color.rgb2fg(*bottom_pixel)}{bg_symbol_fmrt}▄{Color.reset}"
                elif bottom_pixel == sprite_copy.transparent_color:
                    # Only top pixel has color - use upper half block
                    char = f"{Color.rgb2fg(*top_pixel)}{bg_symbol_fmrt}▀{Color.reset}"
                else:
                    # Both pixels have color - combine them
                    char = (f"{Color.rgb2fg(*top_pixel)}"
                           f"{Color.rgb2bg(*bottom_pixel)}"
                           f"▀{Color.reset}")
                
                # Calculate position
                px = origin.x + x + x_offset
                py = origin.y + (y // 2) + y_offset
                
                # Add to render queue
                rq.add_point(Point(px, py), char)
                points.append(Point(px, py))

        return points
    
    def _load_ppm(self, filepath: str) -> tuple:
        """Load PPM file (P3 or P6 format) - unchanged from previous version"""
        with open(filepath, 'rb') as f:
            magic = f.readline().decode('ascii').strip()
            if magic not in ('P3', 'P6'):
                raise ValueError("Unsupported PPM format")
            
            # Read dimensions
            while True:
                line = f.readline().decode('ascii').strip()
                if not line.startswith('#'):
                    break
            width, height = map(int, line.split())
            max_val = int(f.readline().decode('ascii').strip())
            
            # Read pixel data
            pixels = []
            if magic == 'P6':
                data = f.read()
                index = 0
                for _ in range(height):
                    row = []
                    for _ in range(width):
                        row.append((data[index], data[index+1], data[index+2]))
                        index += 3
                    pixels.append(row)
            else:  # P3
                data = []
                for line in f:
                    data.extend(line.decode('ascii').strip().split())
                index = 0
                for _ in range(height):
                    row = []
                    for _ in range(width):
                        r = int(data[index])
                        g = int(data[index+1])
                        b = int(data[index+2])
                        row.append((r, g, b))
                        index += 3
                    pixels.append(row)
        
        return pixels, width, height

class RenderManager:
    def __init__(self, x_size: int, y_size: int, border: bool):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__border = border
        self.__lines = 0
    
    def puts(self, s: str, overwrite: bool = True) -> None:
        if '\n' in s and overwrite:
            self.__lines += 1
        sys.stdout.write(s)

    def display(self, render_queue: RenderQueue, bg_symbol: str, bg_symbol_fmrt: str) -> None:
        if self.__border: self.puts(f"." + ("-"*self.__x_size) + '.\n')
        for y in range(0, self.__y_size):
            if self.__border: self.puts('|')
            for x in range(0, self.__x_size):
                symbol = render_queue.get(Point(x, y))
                if symbol:
                    if '\0' in symbol:
                        symbol = symbol.replace('\0', bg_symbol_fmrt + bg_symbol + Color.reset)
                    self.puts(symbol)
                else:
                    self.puts(bg_symbol_fmrt + bg_symbol + Color.reset)
            if self.__border: self.puts('|')
            self.puts('\n')
        if self.__border: self.puts("`" + ("-"*self.__x_size) + '´\n')

    def flush(self) -> None:
        """ Moves the cursor back to Point(0,0) """
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

    def add_binding(self, key: chr, handler: handler_func) -> None:
        if self.__bindings.get(key):
            raise ValueError(f"Binding for key '{key}' already exists!")
        self.__bindings[key] = handler

    def block_key(self, key: chr) -> None:
        if key not in self.__blocked_keys:
            self.__blocked_keys.append(key)
    
    def allow_key(self, key: chr) -> None:
        if key in self.__blocked_keys:
            self.__blocked_keys.remove(key)

    def update(self) -> None:
        for key in self.__bindings.keys():
            if self.__key_pressed(key): self.__bindings[key](key)

class Scene:
    def __init__(self, tickdelay: float = 0.08, bg_symbol: chr = ' ', bg_symbol_fmrt: str = ''):
        self.tickdelay: float = tickdelay
        self.bg_symbol: chr = bg_symbol
        self.render_queue = RenderQueue()
        self.input_manager = InputManager()
        self.bg_symbol_fmrt = bg_symbol_fmrt

    def setup(self) -> None:
        """ Overwrite this function with your own logic """
        pass

    def update(self) -> None:
        """ Overwrite this function with your own logic """
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

    def cleanup(self) -> None:
        if os.name != 'nt':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__old_settings)

    def quit(self, status: int = None) -> None:
        if status == None:
            status = self.__quit_status
        self.cleanup()
        exit(status)

    def add_scene(self, name: str, scene: Scene) -> None:
        if self.__scenes.get(name):
            raise ValueError(f'A Scene with the name "{name}" already exists!')

        self.__scenes[name] = scene
    
    def set_scene(self, name: str) -> None:
        if not self.__scenes.get(name):
            raise ValueError(f'A Scene with the name "{name}" dose not exists! Add scenes by using the Geme.add_scene function.')

        self.__active_scene = name

    def run(self) -> None:
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

            self.render_manager.display(scene.render_queue, scene.bg_symbol, scene.bg_symbol_fmrt)

            scene.render_queue.clear()
            scene.update()
            scene.input_manager.update()

            self.render_manager.flush()
            sleep(scene.tickdelay)