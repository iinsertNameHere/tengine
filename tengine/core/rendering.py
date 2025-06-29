import math
import sys

from .color import Color, frmt, len_no_ansi, split_and_group_ansi
from .geometry import *

class RenderQueue:
    pass

class RenderQueue:
    def __init__(self, queue: dict[tuple[int, int], str] = {}, bg_symbol: chr = ' ', bg_symbol_frmt: frmt = ''):
        self.__queue: dict[tuple[int, int], str] = queue
        self.bg_symbol = bg_symbol
        self.bg_symbol_frmt = bg_symbol_frmt

    def __repr__(self) -> str:
        return str(self.__queue)
    
    def __str__(self) -> str:
        return str(self.__queue)

    def __add__(self, rq: RenderQueue) -> RenderQueue:
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        d = {}
        d.update(self.__queue)
        d.update(rg.to_dict())
        return RenderQueue(d)

    def __iadd__(self, rq: RenderQueue) -> RenderQueue:
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        self.__queue.update(rq.to_dict())
        return self
        
    def __radd__(self, rq: RenderQueue) -> RenderQueue:
        if type(rq) != type(self):
            raise ValueError(f"{rq} is not of type tengine.RenderQueue!")
        return self.__add__(rq)
    
    def to_dict(self) -> dict[tuple[int, int], str]:
        return self.__queue

    def points(self) -> list[Point]:
        return [Point(p.x, p.y) for p in self.__queue.keys()]
    
    def get(self, point) -> str|None:
        return self.__queue.get((point.x, point.y))
    
    def draw_char(self, point: Point, symbol: str) -> None:
        self.__queue[(point.x, point.y)] = symbol

    def draw_text(self, string: str, origin: Point, center: bool = False) -> None:
        lines = string.split("\n")

        if center:
            origin = Point(origin.x - (len_no_ansi(lines[0]) // 2), origin.y - (len(lines) // 2))

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
            self.draw_char(point, ch)

    def draw_line(self, start: Point, end: Point, symbol: str):
        for p in line(start, end):
            self.draw_char(p, symbol)

    def draw_circle(self, center: Point, radius: int, symbol: str, filled=False, aspect_ratio_compensation: bool = True):
        points = []
        if filled:
            points = filled_circle(center, radius, 0.5 if aspect_ratio_compensation else 1)
        else:
            points = circle(center, radius, 0.5 if aspect_ratio_compensation else 1)

        for p in points:
            self.draw_char(p, symbol)

    def draw_rectangle(self, top_left: Point, width: int, height: int, symbol: str, filled=False):
        points = []
        if filled:
            points = filled_rectangle(top_left, width, height)
        else:
            points = rectangle(top_left, width, height)

        for p in points:
            self.draw_char(p, symbol)

    def draw_triangle(self, point_a: Point, point_b: Point, point_c: Point, symbol: str, filled=False):
        points = []
        if filled:
            points = filled_triangle(point_a, point_b, point_c)
        else:
            points = triangle(point_a, point_b, point_c)

        for p in points:
            self.draw_char(p, symbol)

    def clear(self) -> None:
        self.__queue = {}

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

    def display(self, render_queue: RenderQueue) -> None:
        if self.__border: self.puts(f"." + ("-"*self.__x_size) + '.\n')
        for y in range(0, self.__y_size):
            if self.__border: self.puts('|')
            for x in range(0, self.__x_size):
                symbol = render_queue.get(Point(x, y))
                if symbol:
                    if '\0' in symbol:
                        symbol = symbol.replace('\0', render_queue.bg_symbol_frmt + render_queue.bg_symbol + Color.reset)
                    self.puts(symbol)
                else:
                    self.puts(render_queue.bg_symbol_frmt + render_queue.bg_symbol + Color.reset)
            if self.__border: self.puts('|')
            self.puts('\n')
        if self.__border: self.puts("`" + ("-"*self.__x_size) + '´\n')

    def flush(self) -> None:
        """ Moves the cursor back to Point(0,0) """
        self.puts(f"\033[{self.__lines}A\r")
        self.__lines = 0