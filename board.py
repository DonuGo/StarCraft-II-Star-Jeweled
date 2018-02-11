import cv2 as cv
import numpy as np
from PIL import ImageGrab
import win32con, win32api, win32gui

colors = ['0.png','1.png','2.png','3.png','4.png','5.png']
screenshot_file = "screen_capture.bmp"
colImgs = []


def screenshot(window, file):
    win32gui.SetForegroundWindow(window)
    bbox = win32gui.GetWindowRect(window)
    ImageGrab.grab(bbox).save(file)

def find_matrix(window):
    screenshot(window, screenshot_file)
    screen = cv.imread(screenshot_file,0)
    topImg = cv.imread('top.png',0)
    dowImg = cv.imread('dow.png',0)
    topW, topH = topImg.shape[::-1]
    dowW, dowH = dowImg.shape[::-1]
	
    tmpImg = screen.copy()	
    method = eval('cv.TM_CCOEFF_NORMED')
    res = cv.matchTemplate(tmpImg, topImg, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    if max_val < 0.7: 
        print "Error: Cannot find the top corner"
        exit()

    tmpImg = screen.copy()	
    method = eval('cv.TM_CCOEFF_NORMED')
    res = cv.matchTemplate(tmpImg, dowImg, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    if max_val < 0.7: 
        print "Error: Cannot find the down corner"
        exit()
	
    if max_loc[1] - top_left[1] < 128 or max_loc[0] - top_left[0] < 128:
        print "Error: the size of board is not correct"
        exit()

    return {'top':top_left[1] + topH, 'left':top_left[0] + topW, 'height':max_loc[1] - top_left[1] - topH, 'width':max_loc[0] - top_left[0] - topW}

def find_color(image):
    method = eval('cv.TM_CCOEFF_NORMED')
    for x in range(0, 6):
        colImg = colImgs[x]
        res = cv.matchTemplate(image, colImg, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#        print max_val, max_loc[0], max_loc[1]
        if(max_val > 0.7):
            return x
    return 7
    
def init_board(matrix):
    
    print matrix['top'], matrix['left'], matrix['height'], matrix['width']
    gemSize = [matrix['height'] / 8, matrix['width'] / 8 ]
    print gemSize[0], gemSize[1]
    for x in range(0, 6):
        colImgs.append(cv.imread(colors[x],0))

def fill_table(window, matrix, board):
    screenshot(window, screenshot_file)
    screen = cv.imread(screenshot_file,0)
    gemSize = [matrix['height'] / 8, matrix['width'] / 8 ]
    for x in range(0, 8):
        for y in range(0, 8):
            cropImg = screen[matrix['top'] + x * gemSize[0]:matrix['top'] + (x + 1)* gemSize[0], matrix['left'] + y * gemSize[1]:matrix['left'] + (y + 1)* gemSize[1]]
            board[x][y] = find_color(cropImg)
    print


