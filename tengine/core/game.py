import os
from time import sleep

from .rendering import RenderQueue, RenderManager
from .input import InputManager
from .color import frmt, Color
from .geometry import Point

if os.name != 'nt':
    import tty
    import termios
    import sys


class Scene:
    def __init__(self, tickdelay: float = 0.08, bg_symbol: chr = ' ', bg_symbol_frmt: frmt = ''):
        self.tickdelay: float = tickdelay
        self.render_queue = RenderQueue(bg_symbol = bg_symbol, bg_symbol_frmt = bg_symbol_frmt)
        self.input_manager = InputManager()

    def setup(self) -> None:
        """ Overwrite this function with your own logic """
        pass

    def update(self) -> None:
        """ Overwrite this function with your own logic """
        pass


class Game:
    def __init__(self, width: int, height: int, border: bool = True):
        os.system("") # Prep terminal for formating codes

        if os.name != 'nt':
            self.__old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

        self.__quit_status: int = ""
        self.__scenes: dict[str, Scene] = {}
        self.__active_scene: str = None
        self.x_size = width
        self.y_size = height

        self.render_manager = RenderManager(self.x_size, self.y_size, border)

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

            self.render_manager.display(scene.render_queue)

            scene.render_queue.clear()
            scene.update()
            scene.input_manager.update()

            self.render_manager.flush()
            sleep(scene.tickdelay)