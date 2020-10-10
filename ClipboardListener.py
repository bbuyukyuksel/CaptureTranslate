from pynput import keyboard
import clipboard
import threading
import globals
import time

import datetime

class ClipboardListener(threading.Thread):
    __CTRL = False
    __COPY = False

    __CTRL_Time = None
    __COPY_Time = None

    __clipboard_item = None

    __ftrigger = None
    __clipboard_trigger_counter = 0
    __clipboard_trigger_Times = [None, None]

    wait = threading.Event()

    def __init__(self, handler):
        super().__init__()
        self.__ftrigger = handler
        self.__CTRL_Time = time.time()
        self.__COPY_Time = time.time()

    def __handler(self):
        self.wait.set()
        
        if(time.time() - self.__CTRL_Time > 1):
            #print("debug", "CTRL RESET")
            self.__CTRL = False
        
        if( time.time() - self.__COPY_Time > 1):
            #print("debug", "COPY RESET")
            self.__COPY = False
        
        if (self.__CTRL and self.__COPY and self.__CTRL_Time - self.__COPY_Time < 0.1):    
            self.__clipboard_trigger_Times[self.__clipboard_trigger_counter] = time.time()
            self.__clipboard_trigger_counter += 1

        if (self.__clipboard_trigger_counter == 2):
            self.__clipboard_trigger_counter = 0  

            trigger_diff_time = self.__clipboard_trigger_Times[1] - self.__clipboard_trigger_Times[0]
            
            if(trigger_diff_time <= 2.0):
                time.sleep(0.3)
                try:
                    self.__clipboard_item = clipboard.paste()
                except:
                    self.__clipboard_item = None

                if self.__ftrigger is not None:
                    self.__ftrigger(self.__clipboard_item)
                print("debug", self.__clipboard_item)

                self.__CTRL = False
                self.__COPY = False
            else:
                print("debug", "twice trigger timeout!")
                pass
            
        self.wait.clear()
        
    def on_press(self, key):
        time.sleep(0.5)
        try:
            if key.char == 'c' or key.char == 'C':
                self.__COPY = True
                self.__COPY_Time = time.time()

        except AttributeError:
            if key == keyboard.Key.cmd:
                self.__CTRL = True
                self.__CTRL_Time = time.time()
        print("tetiklendi", datetime.datetime.now())
        if not self.wait.is_set():
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


#region test-code
def myHandler(item):
    print("Item", item)

if __name__ == '__main__':
    ClipboardListener(myHandler).start()
    input('..')
#endregion test-code 