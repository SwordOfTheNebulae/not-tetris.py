from pynput import keyboard
from threading import Lock

class InputHandler: 
    def __init__(self) -> None:
        self.listener = keyboard.Listener(
        on_press=self._on_press,
        on_release=self._on_release)
        self.listener.start()
        self.keys:dict[str|keyboard.Key, int] = {} # values: 0 not pressed, 1 pressed, 2 pressed and processed, -1 unpressed, but not processed: allows for handling keys pressed for less than 1 frame
        self.lockkeys = Lock()
    def _on_press(self, key: keyboard.KeyCode):
        self.lockkeys.acquire()
        try:
            self.keys[key.char] = 1
        except AttributeError:
            self.keys[key] = True
        self.lockkeys.release()

    def _on_release(self,key: keyboard.KeyCode):
        if key == keyboard.Key.delete:
            # Stop listener
            return False
        self.lockkeys.acquire()
        try:
            self.keys[key.char] = -1 if self.keys[key.char] == 1 else 0
        except AttributeError:
            if self.keys.get(key):
                self.keys[key] = -1 if self.keys[key] == 1 else 0
        self.lockkeys.release()
        
    def get_key(self, key):
        val = False
        self.lockkeys.acquire()
        if self.keys.get(key):
            self.keys[key] = 2 if self.keys[key] > 0 else 0
            val = True
        self.lockkeys.release()
        return val
    
    def get_justpressed(self, key):
        val = False
        self.lockkeys.acquire()
        if self.keys.get(key) == 1 or self.keys.get(key) == -1:
            self.keys[key] = 2 if self.keys[key] > 0 else 0
            val = True
        self.lockkeys.release()
        return val

    