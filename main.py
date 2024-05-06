import os
import random

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

board = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]

turn = random.choice([colors.FAIL + "X" + colors.ENDC, colors.OKBLUE + "O" + colors.ENDC])

def showBoard():
    print(f"     |     |      ")
    print(f"  {board[0][0]}  |  {board[0][1]}  |   {board[0][2]}  ")
    print(f"     |     |      ")
    print(f"-----------------")
    print(f"     |     |      ")
    print(f"  {board[1][0]}  |  {board[1][1]}  |   {board[1][2]}  ") 
    print(f"     |     |      ")
    print(f"-----------------")
    print(f"     |     |      ")
    print(f"  {board[2][0]}  |  {board[2][1]}  |   {board[2][2]}  ")
    print(f"     |     |      ")
    print(f"\n")

def placeItem(space):
    if space - 1 < 0 or space > 9:
        return False
    
    if space <= 3:
        if board[0][space-1] != colors.FAIL + "X" + colors.ENDC and board[0][space-1] != colors.OKBLUE + "O" + colors.ENDC:
            board[0][space-1] = turn
        else:
            return False
    elif space <= 6:
        if board[1][space-4] != colors.FAIL + "X" + colors.ENDC and board[1][space-4] != colors.OKBLUE + "O" + colors.ENDC:
            board[1][space-4] = turn
        else:
            return False
    elif space <= 9:
        if board[2][space-7] != colors.FAIL + "X" + colors.ENDC and board[2][space-7] != colors.OKBLUE + "O" + colors.ENDC:
            board[2][space-7] = turn
        else:
            return False
        
    return True

def switchTurn(turn):
    if turn == colors.FAIL + "X" + colors.ENDC:
        return colors.OKBLUE + "O" + colors.ENDC
    else:
        return colors.FAIL + "X" + colors.ENDC
    
def checkWin(board):
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
    
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    
    for x in range(3):
        for y in range(3):
            if freeSpace(x, y, board):
                return False
    
    return "draw"

def freeSpace(x, y, board):
    if board[x][y] != colors.FAIL + "X" + colors.ENDC and board[x][y] != colors.OKBLUE + "O" + colors.ENDC:
        return True
    else:
        return False

def minimax(board, depth, isMax):
    winner = checkWin(board)

    if winner != False:
        if winner == "draw":
            return 0
        else:
            if winner == colors.FAIL + "X" + colors.ENDC:
                return -1
            else:
                return 1
            
    if isMax:
        bestScore = -1000
        for x in range(3):
            for y in range(3):
                if freeSpace(x, y, board):
                    prevName = board[x][y]
                    board[x][y] = colors.OKBLUE + "O" + colors.ENDC
                    score = minimax(board, depth+1, False)
                    board[x][y] = prevName
                    if score > bestScore:
                        bestScore = score
        
        return bestScore
    else:
        bestScore = 1000
        for x in range(3):
            for y in range(3):
                if freeSpace(x, y, board):
                    prevName = board[x][y]
                    board[x][y] = colors.FAIL + "X" + colors.ENDC
                    score = minimax(board, depth+1, True)
                    board[x][y] = prevName
                    if score < bestScore:
                        bestScore = score
        
        return bestScore

def aiTurn():
    bestScore = -1000
    bestMove = [0, 0]
    for x in range(3):
        for y in range(3):
            if freeSpace(x, y, board):
                prevName = board[x][y]
                board[x][y] = colors.OKBLUE + "O" + colors.ENDC
                score = minimax(board, 0, False)
                board[x][y] = prevName
                if score > bestScore:
                    bestScore = score
                    bestMove = [x, y]
    
    board[bestMove[0]][bestMove[1]] = colors.OKBLUE + "O" + colors.ENDC

if __name__ == '__main__':
    while True:
        os.system("clear")
        showBoard()

        winner = checkWin(board)

        if winner != False:
            if winner == "draw":
                print("The game is tied")
                exit(0)
            else:
                print(f"'{winner}' has won the game")
                exit(0)

        if turn == colors.FAIL + "X" + colors.ENDC:
            while True:
                try:
                    selectedSpace = int(input("Where would you like to go? "))
                except ValueError:
                    os.system("clear")
                    showBoard()
                    print("Please select a different space...")
                    continue
                
                if not placeItem(selectedSpace):
                    os.system("clear")
                    showBoard()
                    print("Please select a different space...")
                else:
                    break
        else:
            aiTurn()

        turn = switchTurn(turn)

