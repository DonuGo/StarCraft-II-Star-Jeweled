import time
import win32con, win32api, win32gui
import mouse as Mouse
import board as Board
import strategy as Strategy
from PIL import ImageGrab, Image

def do_move(window, Matrix, moveboard):
    Matrix['top'], Matrix['left'], Matrix['height'], Matrix['width']
    gemSize = [Matrix['height'] / 8, Matrix['width'] / 8 ]
    for x in range(7, -1, -1):
        for y in range(7, -1, -1):
            if moveboard[x][y] > 0 and moveboard[x][y] < 5: 
                dx, dy = Strategy.move_decode(moveboard[x][y])
                targetX = x + dx 
                targetY = y + dy
                Mouse.click(window, Matrix['left'] + gemSize[1] / 2 + gemSize[1] * y,  Matrix['top'] + gemSize[0] / 2 + gemSize[0] * x)
                Mouse.click(window, Matrix['left'] + gemSize[1] / 2 + gemSize[1] * targetY,  Matrix['top'] + gemSize[0] / 2 + gemSize[0] * targetX)
                #return 

def get_window():
    def call(hwnd, param):
        size = win32gui.GetWindowRect(hwnd)
        print win32gui.GetWindowText(hwnd), hash(win32gui.GetWindowText(hwnd))
        if hash(win32gui.GetWindowText(hwnd)) == 786508218 or hash(win32gui.GetWindowText(hwnd)) == -1115897400: # Chinese or English 
            param.append(hwnd)
    winds = []
    win32gui.EnumWindows(call, winds)
    return winds 


def main():
    print "Hello, start game"
    windows = get_window()
    if len(windows) != 1:
        print "Cannot find window"
        exit()
    window = windows[0]

    board = [[0 for x in range(8)] for y in range(8)]
    board2 = [[0 for x in range(8)] for y in range(8)]
    Matrix = Board.find_matrix(window)
    Board.init_board(Matrix)
    while True:
        Board.fill_table(window, Matrix, board)
        Strategy.print_board(board)
        moveboard = Strategy.check_move(board)
#        Strategy.print_board(board)
        do_move(window, Matrix, moveboard)	
        time.sleep(0.5)



if __name__ == "__main__":
    main()