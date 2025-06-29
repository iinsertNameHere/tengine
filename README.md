<div align="center">
    <img src="img/tengine-logo.png" style="width: 250px; margin: 0;">
    <h1>tengine - Terminal based Game Engine</h3>
    <p><a href="#features">Features</a> • <a href="#showcase">Showcase</a> • <a href="#getting-started">Getting Startet</a> • <a href="#module-reference">Module Reference</a> • <a href="#core-concepts">Core Concepts</a> • <a href="#advanced-features">Advanced Features</a> • <a href="#example-games">Example Games</a> • <a href="#roadmap">Roadmap</a> • <a href="#contributing">Contributing</a></p>
</div>

---

<br>

A lightweight, dependency-free engine for creating terminal-based games in Python. Perfect for building text-based adventures, roguelikes, and retro-style games.

```bash
# Quick start
git clone https://github.com/yourusername/tengine.git
cd tengine
python3 snake.py  # Run the example game
```

## Features
- **Cross-platform** - Works on Windows, Linux, and macOS
- **ANSI color support** - Full 16-color support with formatting options
- **Input handling** - Real-time keyboard input without blocking
- **Scene management** - Easy scene transitions and organization
- **Lightweight** - No external dependencies
- **Simple API** - Intuitive object-oriented design

## Showcase
This is an example of what tengine is capable of:
<details>
<summary>Show images 📷</summary>
<div align="left">
    <img style="max-width: 350px" src="img/screenshot1.jpg">
    <img style="max-width: 350px" src="img/screenshot2.jpg">
    <img style="max-width: 550px" src="img/screenshot3.png">
    <img style="max-width: 550px" src="img/screenshot4.png">
    <img style="max-width: 550px" src="img/screenshot5.png">
</div>
</details>

> [!NOTE]  
> Still all running in the terminal. Even the flappybird clone. :)

## Getting Started
```python
from tengine.core import Game, Scene
from tengine.core.geometry import Point
from tengine.core.color import Color

game = Game(width=20, height=10, border=True)

class Hello(Scene):
    def __init__(self):
        super().__init__()

    def update(self):
        self.render_queue.draw_text(f"{Color.fg.green}Hello, tengine!{Color.reset}", Point(2, 1))

if __name__ == "__main__":
    game.add_scene("hello", Hello())
    game.set_scene("hello")
    game.run()
```

Run it with `python3 hello.py`. You just rendered your first colored string!

## Module Reference

### Module `tengine.core.game`

| Class / Method | Signature                                                               | Description                                    |                                       |
| -------------- | ----------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------- |
| **Game**       | `Game(width:int, height:int, border:bool=True)`                         | Initialise a terminal “canvas”.                |                                       |
|                | `.add_scene(name:str, scene:Scene)`                                     | Register a scene object.                       |                                       |
|                | `.set_scene(name:str)`                                                  | Switch active scene (triggers `Scene.setup`).  |                                       |
|                | `.run()`                                                                | Enter the mainloop (blocks).                   |                                       |
|                | `.quit(status:int\|None=None)`                                  | Gracefully restore terminal and exit. |
| **Scene**      | `Scene(tickdelay:float=0.08, bg_symbol:str=' ', bg_symbol_frmt:str='')` | Base class          |                                       |
|                | `.setup()`                                                              | Called once whenever the scene becomes active. |                                       |
|                | `.update()`                                                             | Called every tick; implement game logic here.  |                                       |
|                | `.render_queue`                                                         | Frame buffer for this scene.                   |                                       |
|                | `.input_manager`                                                        | Keyboard handling for this scene.              |                                       |

### Module `tengine.core.rendering`

| Class / Function  | Brief description                                                                                                                                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RenderQueue**   | Off‑screen buffer.  Key methods: <br>`draw_char()`, `draw_text()`, `draw_line()`, `draw_circle()`, `draw_rectangle()`, `draw_triangle()`, `clear()` |
| **RenderManager** | Handles border, displaying the RenderQueue buffer and cursor reset. Internal to `Game`, rarely used directly.                                                                                                                                                                |

### Module `tengine.core.input`

| Item             | Description                                                                                                                |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **InputManager** | Handles user input. Key functions: `add_binding()`, `block_key()`, `allow_key()` |

### Module `tengine.core.color`

* `Color`: nested `fg` / `bg` classes with 16 standard colours plus `rgb(r,g,b)` helpers.
* Formatting flags: `Color.bold`, `Color.underline`, `Color.reverse`, `Color.reset`, …
* `len_no_ansi(text:str) -> int` – correct length of coloured strings.
* `split_and_group_ansi(text:str) -> list[str]` – internal helper; exposed for advanced use.

### Module `tengine.core.geometry`

| Name                                                        | Purpose                                                              |
| ----------------------------------------------------------- | -------------------------------------------------------------------- |
| **Point(x\:int=0, y\:int=0)**                               | Immutable 2‑D point with math (`+`, `-`, comparisons) and `.copy()`. |
| `line(start,end)`                                           | Bresenham line points.                                               |
| `circle(center,r, aspect_ratio=0.5)` / `filled_circle(...)` | Points approximating a circle in terminal cells.                     |
| `rectangle(top_left,w,h)` / `filled_rectangle(...)`         | Points approximating a rectangle in terminal cells.                                                                     | 
| `triangle(a,b,c)` / `filled_triangle(...)`                  | Points approximating a triangle in terminal cells.                                                                     |


## Core Concepts

| Concept              | What it does                                                    | Where to import                        |
| -------------------- | --------------------------------------------------------------- | -------------------------------------- |
| **Game**             | Top‑level controller: window size, active scene, main loop      | `tengine.core.Game`                    |
| **Scene**            | Encapsulates a game state; override `setup()` & `update()`      | `tengine.core.Scene`                   |
| **RenderQueue**      | Off‑screen buffer you draw into each frame                      | `tengine.core.rendering.RenderQueue`   |
| **RenderManager**    | Flushes a queue to the terminal each tick                       | `tengine.core.rendering.RenderManager` |
| **InputManager**     | Non‑blocking keyboard bindings                                  | `tengine.core.input.InputManager`      |
| **Color**            | ANSI helpers (`Color.fg.red`, `Color.bg.blue`, `Color.bold`, …) | `tengine.core.color.Color`             |
| **Geometry** | 2‑D math plus ready‑made shapes                                 | `tengine.core.geometry`   |

---

### Game Class
The main controller for your game:
```python
game = Game(
    width=60,       # Grid width in characters
    hight=30,       # Grid height in characters
    border=True     # Display border around play area
)
```

### Scene Class
Represents different game states (menus, levels, etc.):
```python
class CustomScene(Scene):
    def __init__(self):
        """Initial scene Initialization"""
        super().__init__(
            tickdelay=0.1,              # Tick update interval in seconds
            bg_symbol=' ',              # Background character
            bg_symbol_frmt=Color.bg.red # ANSI Formating for bg_symbol
        )
    
    def setup(self):
        """Initialize scene resources (called each time the game switches to this scene using Game.set_scene)"""
        
    def update(self):
        """Called every tick for game logic"""
```

### Rendering System
Add content to the display:
```python
# Add single character at position
Scene.render_queue.draw_char(Point(3, 4), "#")

# Add multi-line string of characters starting from origin point
Scene.render_queue.draw_text("[----------]", Point(10, 5))

# Format text using Color class
Scene.render_queue.draw_stext(f"{Color.bold}{Color.fg.Red}[ SCORE: 100 ] {Color.reset}", Point(0, 0))

# Draw a line from point a to point b
Scene.render_queue.draw_line(Point(0, 0), Point(5, 5), '#')
```
Each Scene instance has its own render queue which can be accessed via: `self.render_queue`. You can also manipulate a scenes render queue from outside the instance like so: `scene.render_queue`.

### Input Handling
Handle keyboard input:
```python
class GameScene(Scene):
    def __init__(self):
        super().__init__()
        # Bind keys to handler function
        self.input_manager.add_binding('a', self.key_handler_a)
        self.input_manager.add_binding('b', self.key_handler_b)
        self.input_manager.add_binding('c', self.key_handler_c)
        
    def key_handler_a(self):
        # Handle key press

    def key_handler_b(self):
        # Handle key press

    def key_handler_c(self,):
        # Handle key press

    def setup(self):
        # Initialize var when scene is loaded
        self.last_key = "..." # Var to hold last key that was pressed

    def update(self):
        # Display last key that was pressed on screen
        self.render_queue.add_string(f"Last Key Pressed: {self.last_key}", Point(1, 1))
        
```

### Color System
Use ANSI colors for rich visuals:
```python
from tengine.color import Color

# Basic usage
f"{Color.fg.red}Warning! {Color.fg.green}Safe zone{Color.reset}"

# Combine styles
f"{Color.bold}{Color.underline}Important!{Color.reset}"

# Background colors
f"{Color.bg.blue}Water area{Color.reset}"

# Style text with rgb colors
f"{Color.fg.rgb(255, 0, 255)}{Color.bg.rgb(0, 255, 0)}RGB Text!{Color.reset}"
```

## Advanced Features

### ANSI String Handling
```python
from tengine.color import len_no_ansi

text = f"{Color.fg.red}Hello{Color.reset}"
print(len(text)) # Resulting number will be much larger then the text displayed because the ansi codes are also counted as characters.
print(len_no_ansi(text))  # Using len_no_ansi will strip the text of ansi codes before counting the length, which results in the correct number.
```

### Coordinate System
The `Point` class simplifies position math:
```python
p1 = Point(3, 4)
p2 = Point(1, 1)

print(p1 + p2)  # → Point(4, 5)
print(p1 > p2)  # → True
```

## Example Games
### Snake
The repository includes a complete Snake game:
```bash
cp tengine examples/snake
cd examples/snake
python3 snake.py
```
The game gives a simple usage example for tengine.
This includes:
- The coloring system
- Saving game states
- Input management
- Multiple scenes
- Dynamic object rendering

Take a look at [snake.py](examples/snake/snake.py) to lern more about how the game works.

### Flappybord
The repository also includes a complete Flappybord clone:
```bash
cp tengine examples/flappybird
cd examples/flappybird
python3 flappybird.py
```
The game gives a advanced usage example for tengine.
This includes:
- The rgb coloring system
- Saving game states
- Input management
- Multiple scenes
- Dynamic .ppm sprite rendering.
- Collison detection using collider boxes.

Take a look at [flappybird.py](examples/flappybird/flappybird.py) to lern more about how the game works.

## Roadmap
Planned features:
- More example games (Slots, Flappybird)
- Improved documentation
- Entity component system (ECS)

## Contributing
Contributions are welcome! Thx 💜

<a href = "https://github.com/iinsertNameHere/tengine/graphs/contributors">
    <img src = "https://contrib.rocks/image?repo=iinsertNameHere/tengine">
</a>

## License


`tengine` is distributed under the MIT License (see [`LICENSE`](LICENSE)).

<br>
<br>

---

<div align="center">
    <img src="https://api.lucabubi.me/chart?username=iinsertNameHere&repository=tengine">
</div>