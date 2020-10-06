from pynput import keyboard
import clipboard
import threading
import globals
import time

class ClipboardListener(threading.Thread):
    __CTRL = False
    __COPY = False
    __clipboard_item = None

    __ftrigger = None

    def __init__(self, handler):
        super().__init__()
        self.__ftrigger = handler

    def __handler(self):
        if (self.__CTRL and self.__COPY):    
            time.sleep(0.3)
            self.__clipboard_item = clipboard.paste()
            
            if self.__ftrigger is not None:
                self.__ftrigger(self.__clipboard_item)
            print("item-debug", self.__clipboard_item)

            self.__CTRL = False
            self.__COPY = False


    def on_press(self, key):
        try:
            if key.char == 'c' or key.char == 'C':
                self.__COPY = True
                print("Copy")

        except AttributeError:
            if key == keyboard.Key.cmd:
                self.__CTRL = True
                print("Ctrl")
        self.__handler()

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            print("Stop Listener")
            globals.wait.set()
            return False

    def run(self):
        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release)
        listener.start()


def myHandler(item):
    print("Item", item)

if __name__ == '__main__':
    ClipboardListener(myHandler).start()
    input('..')