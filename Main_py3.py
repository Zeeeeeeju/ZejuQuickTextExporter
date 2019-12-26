import win32con
import ctypes
import ctypes.wintypes
from threading import Thread
import requests
import pyperclip

h_ids = [i for i in range(2)]
h_keys = {i: False for i in h_ids}
h_dict = {}

class Hotkey(Thread):
    user32 = ctypes.windll.user32

    def regiskey(self, hwnd=None, flagid=0, fnkey=win32con.MOD_ALT, vkey=win32con.VK_F9):
        return self.user32.RegisterHotKey(hwnd, flagid, fnkey, vkey)

    def callback(self, id, func):
        h_dict[id] = func
        def inner():
            while True:
                for key, value in h_dict.items():
                    if h_keys[h_ids[key]]:
                        thread_it(value)
                        h_keys[h_ids[key]] = False
        return inner

    def run(self):
        if not self.regiskey(None, h_ids[0], 0, win32con.VK_F4):
            print(f"热键注册失败！ id{h_ids[0]}")
        try:
            msg = ctypes.wintypes.MSG()
            while True:
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam in h_ids:
                            h_keys[msg.wParam] = True
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            for i in h_ids:
                self.user32.UnregisterHotKey(None, i)

def thread_it(func, *args):
    t = Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

def have_fun():
    url = "https://nmsl.shadiao.app/api.php?lang=zh_cn"
    res = requests.get(url).text

    pyperclip.copy(res)

if __name__ == '__main__':
    hotkey = Hotkey()
    hotkey.start()
    fn = hotkey.callback(0, have_fun)
    thread_it(fn)
