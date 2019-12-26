import pyhk
import pyperclip
import requests

hot_handle = pyhk.pyhk()
hot_key = ['F4']
change_key = ['Ctrl','Q']

def fun():
    url = "https://nmsl.shadiao.app/api.php?lang=zh_cn"
    res = requests.get(url).text

    pyperclip.copy(res)

def changeKey():
    print("fu")


hot_handle.addHotkey(hot_key, fun)
hot_handle.addHotkey(change_key, changeKey)

hot_handle.start()
