import shutil
import os
import random
import time
import json

from tengine.core import Game, Scene
from tengine.core.geometry import Point, rectangle
from tengine.core.rendering import RenderQueue, RenderManager
from tengine.core.color import Color, len_no_ansi

from tengine.advanced.sprites import SpriteManager
from tengine.misc.keys import Key

os.system("clear")
x, y = shutil.get_terminal_size((100, 30))

game = Game(x, y - 1, False)
center_point = Point(int(game.x_size / 2), int(game.y_size / 2))

sprite_manager = SpriteManager()
sprite_manager.load_sprite("bird1", "bird1.ppm", (0, 255, 0))
sprite_manager.load_sprite("bird2", "bird2.ppm", (0, 255, 0))
sprite_manager.load_sprite("pipe_end", "pipe_end.ppm", (0, 255, 0))
sprite_manager.load_sprite("pipe_body", "pipe_body.ppm", (0, 255, 0))
sprite_manager.load_sprite("gameover", "gameover.ppm", (0, 255, 0))
sprite_manager.load_sprite("flappybird", "flappybird.ppm", (0, 255, 0))

highscore = 0
last_score = 0

class Menu(Scene):
    def __init__(self):
        super().__init__(0.04, bg_symbol_frmt=Color.bg.rgb(69, 163, 239))

        self.input_manager.add_binding(Key.KEY_Q, self.save_and_quit)
        self.input_manager.add_binding(Key.KEY_SPACE, lambda: game.set_scene("play"))

        self.bird_pos = Point(25, center_point.y)
        self.bird_flap = False
        self.bird_flap_frame = 0
        self.pipe_x_positions = [center_point.x - 40, center_point.x, center_point.x + 40]
        self.pipe_randints = [(random.randint(-5, 5),random.randint(5, 20))for _ in range(len(self.pipe_x_positions)) ]


    def save_and_quit(self):
        global last_score, highscore
        with open("flappybird_save.json", "w") as f:
            json.dump({"last_score": last_score, "highscore": highscore}, f)
        game.quit()

    def draw_pipes(self):
        for i, start_x in enumerate(self.pipe_x_positions):
            origin = center_point.y + self.pipe_randints[i][0]
            pipe_point = Point(start_x, origin + self.pipe_randints[i][1])

            sprite_manager.render_sprite(self.render_queue, "pipe_end", pipe_point, True)

            body_point = pipe_point.copy()
            while body_point.y < game.y_size - 1:
                body_point.y += 10
                sprite_manager.render_sprite(self.render_queue, "pipe_body", body_point, True)

    def setup(self):
        self.bird_flap = False
    
    def update(self):

        self.draw_pipes()

        sprite_manager.render_sprite(self.render_queue, "flappybird", Point(center_point.x, 10), True)
        
        self.render_queue.draw_text(
            f"{self.render_queue.bg_symbol_frmt}{Color.bold}{Color.fg.rgb(255, 255, 255)}Press {Color.bg.rgb(255, 211, 92)}{Color.fg.rgb(0, 0, 0)}SPACE{Color.reset}{self.render_queue.bg_symbol_frmt}{Color.bold}{Color.fg.rgb(255, 255, 255)} to PLay  or {Color.bg.rgb(255, 211, 92)}{Color.fg.rgb(0, 0, 0)}Q{Color.reset}{self.render_queue.bg_symbol_frmt}{Color.bold}{Color.fg.rgb(255, 255, 255)} to Quit...{Color.reset}", 
            center_point, center=True)
        
        sprite_manager.render_sprite(self.render_queue, "bird2" if self.bird_flap else "bird1", self.bird_pos, True)
        self.render_queue.draw_line(Point(0, game.y_size - 1), Point(game.x_size, game.y_size - 1), f"{Color.fg.rgb(0, 0, 0)}{Color.bg.rgb(206, 185, 144)}▀{Color.reset}")

        self.render_queue.draw_text(f"{Color.bg.black}{Color.bold}[ LAST SCORE: {Color.fg.red}{last_score}{Color.reset}{Color.bg.black}{Color.bold} ]{Color.reset}", Point(2, 1))
        self.render_queue.draw_text(f"{Color.bg.black}{Color.bold}[ HIGHSCORE:  {Color.fg.red}{highscore}{Color.reset}{Color.bg.black}{Color.bold} ]{Color.reset}", Point(2, 2))


        if self.bird_flap:
            self.bird_flap_frame += 1

        if self.bird_flap_frame > 2:
            self.bird_flap_frame = 0
            self.bird_flap = not self.bird_flap

        self.bird_flap_frame += 1

class Play(Scene):
    def __init__(self):
        super().__init__(0.04, bg_symbol_frmt=Color.bg.rgb(69, 163, 239))
        self.input_manager.add_binding(Key.KEY_SPACE, self.handle_space)
        self.input_manager.allow_key(Key.KEY_SPACE)
        self.bird_pos = Point(25, center_point.y)
        self.bird_vilocity = 0
        self.bird_flap = False
        self.bird_flap_frame = 0
        self.pipes = []
        self.pipe_space = 50
        self.gameover = False
        self.score = 0

    def flap(self):
        if self.bird_vilocity > 1.5:
            self.bird_vilocity = -4
        else:
            self.bird_vilocity -= 3
        self.bird_flap = True
                

    def handle_space(self):
        global highscore, last_score
        if self.gameover:
            last_score = self.score
            if self.score > highscore: highscore = self.score
            game.set_scene("menu")
        else:
            self.flap()

    def spawn_pipe(self):
        pipe_type = random.choice(['top', 'bottom', 'double'])
        points = []
        start_x = game.x_size + 5
        
        if pipe_type == "top":
            pipe_point = Point(start_x, (center_point.y - 5) - random.randint(5, 30))

            points.append(("top_end", pipe_point.copy()))

            while pipe_point.y > 0:
                pipe_point.y -= 10
                points.append(("body", pipe_point.copy()))                

        elif pipe_type == "bottom":
            pipe_point = Point(start_x, (center_point.y - 5) + random.randint(5, 30))

            points.append(("bottom_end", pipe_point.copy()))
            
            while pipe_point.y < game.y_size - 10:
                pipe_point.y += 10
                points.append(("body", pipe_point.copy()))

        elif pipe_type == "double":
            origin = center_point.y + random.randint(-5, 5)
            top_pipe_point = Point(start_x, origin - random.randint(10, 20))
            bottom_pipe_point = Point(start_x, origin + random.randint(10, 20))

            points.append(("top_end", top_pipe_point.copy()))
            points.append(("bottom_end", bottom_pipe_point.copy()))

            while top_pipe_point.y > 0:
                top_pipe_point.y -= 10
                points.append(("body", top_pipe_point.copy()))
            while bottom_pipe_point.y < game.y_size - 10:
                bottom_pipe_point.y += 10
                points.append(("body", bottom_pipe_point.copy()))
        
        self.pipes.append([points, False])

    def update_pipes(self):
        if len(self.pipes) == 0:
            self.spawn_pipe()
        
        if self.pipes[-1][0][0][1].x <= (game.x_size + 5) - self.pipe_space:
            self.spawn_pipe()

        del_pipes = []

        for i, pipe in enumerate(self.pipes):
            for j, section in enumerate(pipe[0]):
                if not self.gameover: self.pipes[i][0][j][1].x -= 2

                if section[0] == "top_end":
                    sprite_manager.render_sprite(self.render_queue, "pipe_end", section[1], False, flip_v=True)
                elif section[0] == "bottom_end":
                    sprite_manager.render_sprite(self.render_queue, "pipe_end", section[1], False)
                elif section[0] == "body":
                    sprite_manager.render_sprite(self.render_queue, "pipe_body", section[1], False)

                if self.pipes[i][0][j][1].x <= -20 and i not in del_pipes:
                    del_pipes.append(i)
            
            if pipe[0][0][1].x <= 5 and not self.pipes[i][1]:
                self.pipes[i][1] = True
                self.score += 1

        for i in del_pipes:
            self.pipes.pop(i)

    def check_ground_collisiton(self):
        if self.bird_pos.y + 2 >= game.y_size:
            return True
        return False

    def check_pipe_collisiton(self):
        bird_collisiton_box = rectangle(Point(self.bird_pos.x - (17 // 2) - 2, self.bird_pos.y - 3), 17, 6)
        for pipe in self.pipes:
            if pipe[0][0][1].x <= 50:
                for section in pipe[0]:
                    section_collisiton_box = rectangle(section[1], 20, 10)
                    for bp in bird_collisiton_box:
                        if bp in section_collisiton_box:
                            return True
        return False
    
    def check_collisiton(self):
        if self.check_ground_collisiton() or self.check_pipe_collisiton():
            self.gameover = True
            self.input_manager.block_key(Key.KEY_SPACE)

    def setup(self):
        self.input_manager.allow_key(Key.KEY_SPACE)
        self.bird_pos = Point(25, center_point.y)
        self.bird_vilocity = 0
        self.bird_flap = False
        self.bird_flap_frame = 0
        self.pipes = []
        self.pipe_space = 50
        self.gameover = False
        self.score = 0

    def update(self):
        if self.bird_vilocity > 3:
            self.bird_vilocity = 3
        elif self.bird_vilocity < -4:
            self.bird_vilocity = -4
        
        # Update position based on velocity
        self.bird_pos.y += int(self.bird_vilocity / 2)  # Note the minus sign here

        # Apply gravity (increases velocity downward)
        self.bird_vilocity += 1.25
        
        # Keep the bird within screen bounds
        if self.bird_pos.y < 0:
            self.bird_pos.y = 0
        if self.bird_pos.y >= game.y_size:
            self.bird_pos.y = game.y_size - 1
        
        sprite_manager.render_sprite(self.render_queue, "bird2" if self.bird_flap else "bird1", self.bird_pos, True)

        self.update_pipes()

        self.render_queue.draw_line(Point(0, game.y_size - 1), Point(game.x_size, game.y_size - 1), f"{Color.fg.rgb(0, 0, 0)}{Color.bg.rgb(206, 185, 144)}▀{Color.reset}")

        self.check_collisiton()

        if self.bird_flap:
            self.bird_flap_frame += 1

        if self.bird_flap_frame > 2:
            self.bird_flap_frame = 0
            self.bird_flap = False

        if self.gameover:
            sprite_manager.render_sprite(self.render_queue, "gameover", Point(center_point.x, 10), True)
            if self.check_ground_collisiton():
                self.render_queue.draw_text(
                    f"{self.render_queue.bg_symbol_frmt}{Color.bold}{Color.fg.rgb(255, 255, 255)}Press {Color.bg.rgb(255, 211, 92)}{Color.fg.rgb(0, 0, 0)}SPACE{Color.reset}{self.render_queue.bg_symbol_frmt}{Color.bold}{Color.fg.rgb(255, 255, 255)} to continue...{Color.reset}",
                    center_point, center=True)
                self.input_manager.allow_key(Key.KEY_SPACE)

        self.render_queue.draw_text(f"{Color.bg.black}{Color.bold}[ SCORE: {Color.fg.red}{self.score}{Color.reset}{Color.bg.black}{Color.bold} ]{Color.reset}", Point(2, 1))

if __name__ == '__main__':
    game.add_scene("menu", Menu())
    game.add_scene("play", Play())
    game.set_scene("menu")

    if os.path.exists("flappybird_save.json"):
        with open("flappybird_save.json", "r") as f:
            data = json.load(f)
            last_score = data["last_score"]
            highscore = data["highscore"]

    game.run()