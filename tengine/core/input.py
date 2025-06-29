import os
if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios
    import sys

def handler_function():
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
            if self.__key_pressed(key): self.__bindings[key]()