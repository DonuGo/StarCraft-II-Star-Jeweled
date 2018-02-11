import random

def print_board(board):
    for x in range(0, 8):
        for y in range(0, 8):
            print board[x][y],
        print
    print
	
def find_scoreV(board, x, y):
    score = 1
    index = 0
    for i in range(x - 1, -1, -1):
        if board[x][y] == board[i][y]:
            score += 1
        else:
            index = i + 1
            break
    for i in range(x + 1, 8):
        if board[x][y] == board[i][y]:
            score += 1
        else:
            break
    if score < 3:
	    score = 0
    return score,index

def find_scoreH(board, x, y):
    score = 1
    index = 0
    for i in range(y - 1, -1, -1):
        if board[x][y] == board[x][i]:
            score += 1
        else:
            index = i + 1
            break
    for i in range(y + 1, 8):
        if board[x][y] == board[x][i]:
            score += 1
        else:
            break
    if score < 3:
	    score = 0
    return score,index

def find_score(board, x, y):
    scoreV, indexV = find_scoreV(board, x, y)
    scoreH, indexH = find_scoreH(board, x, y)
    return scoreV + scoreH
	
def move_decode(move):
    if move == 1:
	    return -1, 0
    if move == 2:
	    return 1, 0
    if move == 3:
	    return 0, -1
    if move == 4:
	    return 0, 1
    return 0, 0	

def mark(board, x, y, move):
    dx,dy = move_decode(move)
    board[x][y], board[x+dx][y+dy] = board[x+dx][y+dy], board[x][y]
    scoreV, indexV = find_scoreV(board, x+dx, y+dy)
    scoreH, indexH = find_scoreH(board, x+dx, y+dy)

    for i in range(indexV, indexV + scoreV):
        board[i][y+dy] = 7
    for i in range(indexH, indexH + scoreH):
        board[x+dx][i] = 7
    board[x][y] = 7

def find_move(board, x, y):
    if board[x][y] == 7:
        return 0, 0

    score = [0 for i in range(5)]
    for move in range(1, 5):
        dx,dy = move_decode(move)
        if x + dx < 0 or x + dx > 7 or y + dy < 0 or y + dy > 7:
            continue
        if board[x][y] == board[x+dx][y+dy] or board[x+dx][y+dy] == 7:
            continue 
        board[x][y], board[x+dx][y+dy] = board[x+dx][y+dy], board[x][y]
        score[move] = find_score(board, x+dx, y+dy)
        board[x][y], board[x+dx][y+dy] = board[x+dx][y+dy], board[x][y]

    if max(score) >= 3:
        mark(board, x, y, score.index(max(score)))
	
    return max(score), score.index(max(score))

def check_move(board):
    scoreboard = [[0 for x in range(8)] for y in range(8)]
    moveboard = [[-1 for x in range(8)] for y in range(8)]
    for x in range(0, 8):
        for y in range(0, 8):
            scoreboard[x][y],moveboard[x][y] = find_move(board, x, y)
    return moveboard