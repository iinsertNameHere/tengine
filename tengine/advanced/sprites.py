from ..core.color import Color, frmt, extract_bg_colors
from ..core.geometry import Point
from ..core.rendering import RenderQueue

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

    def copy(self):
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
    ):
        """Render sprite to render queue using half-block characters with transparency"""
        sprite = self.sprites[sprite_name]
        
        # Create flipped copy if needed
        sprite_copy = sprite.copy().flip(flip_h, flip_v)
        
        # Calculate offsets if centering
        x_offset = -sprite_copy.width // 2 if center_origin else 0
        y_offset = -sprite_copy.height // 4 if center_origin else 0  # Divided by 4 because we're combining 2 rows

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
                
                # Calculate position
                px = origin.x + x + x_offset
                py = origin.y + (y // 2) + y_offset

                bg = rq.bg_symbol_frmt
                current_chr = rq.get(Point(px, py))
                if current_chr: 
                    bg_colors = extract_bg_colors(current_chr)
                    if len(bg_colors) > 0:
                        bg = bg_colors[-1]

                # Create colored half-block characterColor
                if top_pixel == sprite_copy.transparent_color:
                    # Only bottom pixel has color - use lower half block
                    char = f"{Color.fg.rgb(*bottom_pixel)}{bg}▄{Color.reset}"
                elif bottom_pixel == sprite_copy.transparent_color:
                    # Only top pixel has color - use upper half block
                    char = f"{Color.fg.rgb(*top_pixel)}{bg}▀{Color.reset}"
                else:
                    # Both pixels have color - combine them
                    char = (f"{Color.fg.rgb(*top_pixel)}"
                           f"{Color.bg.rgb(*bottom_pixel)}"
                           f"▀{Color.reset}")
                
                # Add to render queue
                rq.draw_char(Point(px, py), char)
    
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