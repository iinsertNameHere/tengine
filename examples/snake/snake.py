from time import sleep
import random
import json
import os

from tengine.core import Game, Scene
from tengine.core.geometry import Point
from tengine.core.color import Color, len_no_ansi

game = Game(42, 20)

center_point = Point(int(game.x_size / 2), int(game.y_size / 2))
highscores = {"EASY": 0, "NORMAL": 0, "HARD": 0, "ULTRA": 0}
mode_idx = 1
modes = [("EASY", 0.18), ("NORMAL", 0.13), ("HARD", 0.07), ("ULTRA", 0.04)]

class Menu(Scene):
    def __init__(self):
        super().__init__(0.1, ' ')
        self.input_manager.add_binding('q', self.save_and_quit)
        self.input_manager.add_binding('p', lambda: game.set_scene("play"))
        self.input_manager.add_binding('+', self.raise_mode)
        self.input_manager.add_binding('-', self.lower_mode)
        self.logo = [
            "                           ",
            f"{Color.fg.green}    ____          __       {Color.reset}",
            f"{Color.fg.green}   / __/__  ___ _/ /_____  {Color.reset}",
            f"{Color.fg.green}  _\\ \\/ _ \\/ _ `/  '_/ -_) {Color.reset}",
            f"{Color.fg.green} /___/_//_/\\_,_/_/\\_\\\\__/  {Color.reset}",
            f"{Color.fg.lightblue}  Snake made using tengine {Color.reset}",
            "                           ",
            f"   {Color.fg.black}{Color.bold}{Color.bg.purple}[P - Play]{Color.reset}  {Color.fg.black}{Color.bold}{Color.bg.red}[Q - Quit]{Color.reset}  "
        ]

    def save_and_quit(self):
        with open("snake_save.json", "w") as f:
            json.dump(highscores, f)
        game.quit()

    def raise_mode(self):
        global mode_idx
        mode_idx += 1
        if mode_idx > len(modes) - 1: mode_idx = len(modes) - 1
    
    def lower_mode(self):
        global mode_idx
        mode_idx -= 1
        if mode_idx < 0: mode_idx = 0

    def setup(self):
        pass

    def update(self):

        # Draw Highscore
        self.render_queue.draw_text(
            f"[ {Color.bold}HIGHSCORE: {Color.fg.green}{highscores[modes[mode_idx][0]]}{Color.reset} ]",
            Point(center_point.x, 2), center=True
        )

        # Draw Logo
        self.render_queue.draw_text('\n'.join(self.logo), center_point, center=True)

        mode = modes[mode_idx][0]
        if len(mode) < 7:
            mode = mode + " "*(6 - len(mode))

        # Draw Mode
        self.render_queue.draw_text(
            f"{Color.fg.green} [-]{Color.reset} [ {Color.bold}MODE: {Color.fg.lightblue}{mode}{Color.reset} ] {Color.fg.green}[+] {Color.reset}", 
            Point(center_point.x, center_point.y + 5), center=True)
        

class Play(Scene):
    def __init__(self):
        super().__init__(bg_symbol=f'.', bg_symbol_frmt=Color.fg.darkgrey)
        # Input bindings
        self.input_manager.add_binding('w', lambda: self.set_direction("up"))
        self.input_manager.add_binding('a', lambda: self.set_direction("left"))
        self.input_manager.add_binding('s', lambda: self.set_direction("down"))
        self.input_manager.add_binding('d', lambda: self.set_direction("right"))
    
    def set_direction(self, new_dir):
        # Prevent 180-degree turns
        opposites = {"up":"down", "down":"up", "left":"right", "right":"left"}
        if new_dir != opposites.get(self.direction, ""):
            self.direction = new_dir

    def spawn_food(self):
        while True:
            x = random.randint(1, game.x_size-2)
            y = random.randint(1, game.y_size-2)
            self.food = Point(x, y)
            if self.food not in self.snake:
                break

    def setup(self):
        self.tickdelay = modes[mode_idx][1]
        self.direction = "right"
        self.snake = [center_point.copy(), 
                     Point(center_point.x-1, center_point.y),
                     Point(center_point.x-2, center_point.y)]
        self.score = 0
        self.frame_counter = 0
        self.spawn_food()

    def update(self):
        global highscore
        self.frame_counter += 1

        # Move snake only on even frames for vertical movement
        head = self.snake[0].copy()
        if self.direction == "up":
            head.y -= 1 
        elif self.direction == "down":
            head.y += 1
        elif self.direction == "left":
            head.x -= 1
        elif self.direction == "right":
            head.x += 1
        
        # Check collisions
        if (head.x < 0 or head.x > game.x_size-1 or
            head.y < 0 or head.y > game.y_size-1 or
            head in self.snake):
            sleep(0.5)
            game.set_scene("menu")
            return

        # Add new head
        self.snake.insert(0, head)
        
        # Check food collision
        if head == self.food:
            self.score += 1
            highscores[modes[mode_idx][0]] = max(highscores[modes[mode_idx][0]], self.score)
            self.spawn_food()
        else:
            self.snake.pop()  # Remove tail if no food eaten

        # Render score
        self.render_queue.draw_text(
            f"[ {Color.bold}SCORE: {Color.fg.lightblue}{self.score}{Color.reset} ]",
            Point(center_point.x, 2), center=True)
        
        # Render food
        self.render_queue.draw_char(self.food, f"{Color.fg.red}${Color.reset}")
        
        # Render snake
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                self.render_queue.draw_char(Point(int(segment.x), int(segment.y)), f"{Color.fg.green}@{Color.reset}")
            else:  # Body
                self.render_queue.draw_char(Point(int(segment.x), int(segment.y)), f"{Color.fg.green}O{Color.reset}")

if __name__ == '__main__':
    game.add_scene("menu", Menu())
    game.add_scene("play", Play())
    game.set_scene("menu")

    if os.path.exists("snake_save.json"):
        with open("snake_save.json", "r") as f:
            highscores = json.load(f)

    game.run()