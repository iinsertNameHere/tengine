import math

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
        return (self.x, self.y) >= (p.x, p.y)
    
    def __le__(self, p: Point) -> bool:
        if type(p) != type(self):
            raise ValueError(f"{p} is not of type tengine.Point!")
        return (self.x, self.y) <= (p.x, p.y)

    def copy(self):
        """ Returns a Copy of this point """
        return Point(self.x, self.y)

def line(start: Point, end: Point) -> list[Point]:
    """Generate points along a line between two points"""
    points = []
    x0, y0 = start.x, start.y
    x1, y1 = end.x, end.y
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
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
    
    return points

def circle(center: Point, radius: int, aspect_ratio: float = 0.5) -> list[Point]:
    """Generate points for a circle outline"""
    points = []
    scaled_radius = radius * (1 / aspect_ratio)
    
    for angle in range(0, 360, 2):  # 2° steps
        rad = math.radians(angle)
        x = round(center.x + scaled_radius * math.cos(rad))
        y = round(center.y + radius * math.sin(rad))
        points.append(Point(x, y))
    
    return points

def filled_circle(center: Point, radius: int, aspect_ratio: float = 0.5) -> list[Point]:
    """Generate points for a filled circle"""
    points = []
    scaled_radius = radius * (1 / aspect_ratio)
    min_y = center.y - radius
    max_y = center.y + radius
    
    for y in range(min_y, max_y + 1):
        y_rel = (y - center.y)
        if abs(y_rel) > radius:
            continue
            
        x_width = math.sqrt(radius**2 - y_rel**2) * (1 / aspect_ratio)
        x_start = round(center.x - x_width)
        x_end = round(center.x + x_width)
        
        for x in range(x_start, x_end + 1):
            points.append(Point(x, y))
    
    return points

def rectangle(top_left: Point, width: int, height: int) -> list[Point]:
    """Generate points for rectangle outline"""
    points = []
    x1, y1 = top_left.x, top_left.y
    x2, y2 = x1 + width - 1, y1 + height - 1

    # Horizontal lines
    for x in range(x1, x2 + 1):
        points.append(Point(x, y1))
        points.append(Point(x, y2))
    
    # Vertical lines
    for y in range(y1 + 1, y2):
        points.append(Point(x1, y))
        points.append(Point(x2, y))
    
    return points

def filled_rectangle(top_left: Point, width: int, height: int) -> list[Point]:
    """Generate points for filled rectangle"""
    points = []
    x1, y1 = top_left.x, top_left.y
    x2, y2 = x1 + width, y1 + height

    for y in range(y1, y2):
        for x in range(x1, x2):
            points.append(Point(x, y))
    
    return points

def triangle(point_a: Point, point_b: Point, point_c: Point) -> list[Point]:
    """Generate points for triangle outline"""
    points = []
    points.extend(line(point_a, point_b))
    points.extend(line(point_b, point_c))
    points.extend(line(point_c, point_a))
    return points

def filled_triangle(point_a: Point, point_b: Point, point_c: Point) -> list[Point]:
    """Generate points for filled triangle"""
    points = []
    min_x = min(point_a.x, point_b.x, point_c.x)
    max_x = max(point_a.x, point_b.x, point_c.x)
    min_y = min(point_a.y, point_b.y, point_c.y)
    max_y = max(point_a.y, point_b.y, point_c.y)

    def sign(a: Point, b: Point, c: Point) -> float:
        return (a.x - c.x) * (b.y - c.y) - (b.x - c.x) * (a.y - c.y)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            d_a = sign(p, point_a, point_b)
            d_b = sign(p, point_b, point_c)
            d_c = sign(p, point_c, point_a)

            has_neg = (d_a < 0) or (d_b < 0) or (d_c < 0)
            has_pos = (d_a > 0) or (d_b > 0) or (d_c > 0)

            if not (has_neg and has_pos):
                points.append(p)
    
    return points