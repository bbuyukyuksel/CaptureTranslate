from pynput import keyboard
import clipboard
import threading
import globals
import time
import sys
import datetime

from GUI import DBList

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
                # Process Clipboard Data
                self.process()
                self.__CTRL = False
                self.__COPY = False
            else:
                print("debug", "twice trigger timeout!")
                pass
        self.wait.clear()
    
    def process(self):
        try:
            self.__clipboard_item = clipboard.paste()
        except:
            self.__clipboard_item = None

        if self.__ftrigger is not None:
            self.__ftrigger(self.__clipboard_item)
        print("debug", self.__clipboard_item)
    
    
    #windows-test
    def on_activate_copy(self):
        self.__COPY = True
        self.__COPY_Time = time.time()
        self.__CTRL = True
        self.__CTRL_Time = time.time()
        #print("tetiklendi", datetime.datetime.now(),self.__CTRL, self.__COPY)
        if not self.wait.is_set():
            self.__handler()
   
    def on_press(self, key):
        try:
            print("c", key.char)
            if key.char == 'c' or key.char == 'C':
                self.__COPY = True
                self.__COPY_Time = time.time()

        except AttributeError:
            print("Speacial", key)
            command_key = None
            if sys.platform.startswith("win"):
                command_key = keyboard.Key.ctrl_l
            elif sys.platform.startswith("darwin"):
                command_key = keyboard.Key.cmd
            if key == command_key:
                print("Command Key")
                self.__CTRL = True
                self.__CTRL_Time = time.time()
        print("tetiklendi", datetime.datetime.now(),self.__CTRL, self.__COPY)
        if not self.wait.is_set():
            self.__handler()

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            print("Stop Listener")
            return False

    def run(self):
        # Set Keyboard Listener
        listener = None
        if sys.platform.startswith('win'):
            listener = keyboard.GlobalHotKeys({
                '<ctrl>+c':self.on_activate_copy,
                #'<ctrl>+b':self.on_activate_wordlist,
            })
        else:
            # OS-X
            listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()


#region test-code
def myHandler(item):
    print("Item", item)

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        def on_activate_ctrl_c():
            print('<ctrl>+<c> pressed')
        def on_activate_h():
            print('<ctrl>+<alt>+h pressed')

        def on_activate_i():
            print('<ctrl>+<alt>+i pressed')

        listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+h': on_activate_h,
            '<ctrl>+<alt>+i': on_activate_i,
            '<ctrl>+c':on_activate_ctrl_c})
        listener.start()
        listener.join()    
    else:
        ClipboardListener(myHandler).start()
        ClipboardListener.join()


#endregion test-code 