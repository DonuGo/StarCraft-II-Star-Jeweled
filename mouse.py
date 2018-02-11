import win32con, win32api, win32gui
import time
from PIL import ImageGrab, Image

def click(window, x, y):
    lParam = win32api.MAKELONG(x, y)
    win32gui.PostMessage (window, win32con.WM_LBUTTONDOWN , win32con.MK_LBUTTON, lParam);
    win32gui.PostMessage (window, win32con.WM_LBUTTONUP, 0, lParam);