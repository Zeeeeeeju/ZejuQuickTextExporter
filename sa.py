import win32api, win32con, win32gui
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


def send_input_hax(hwnd, msg):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN , 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN , 0)
    for c in msg:
        if c == "\n":
            win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN , 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN , 0)

def main():
    client_hwnd = []
    win32gui.EnumWindows(callback, client_hwnd)
    print("Client hwnd", client_hwnd)
    if len(client_hwnd) != 1:
        print("Game client not open.")
    else:
        send_input_hax(client_hwnd[0], "啊啊啊")

def have_fun():
    # url = "https://nmsl.shadiao.app/api.php?lang=zh_cn"
    # res = requests.get(url).text
    send_input_hax(client_hwnd[0], "啊啊啊")

def callback(hwnd, client_hwnd):
    if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
        print(win32gui.GetWindowText(hwnd))
        print(hwnd)
        if win32gui.GetWindowText(hwnd).find('League of Legends (TM) Client') != -1:
            client_hwnd.append(hwnd)
        if win32gui.GetWindowText(hwnd).find("QQ") != -1:
            print("bbbb")
            client_hwnd.append(hwnd)
        #client_hwnd.append(win32gui.GetWindowText(hwnd))

if __name__ == '__main__':
    hotkey = Hotkey()
    hotkey.start()
    client_hwnd = []
    win32gui.EnumWindows(callback, client_hwnd)
    fn = hotkey.callback(0, have_fun)
    thread_it(fn)