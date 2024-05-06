import os
import random

class colors:
    blue = '\033[94m'
    red = '\033[91m'
    endl = '\033[0m'
    bold = '\033[1m'

board = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]

turn = random.choice([colors.red + "X" + colors.endl, colors.blue + "O" + colors.endl])

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

def output(string):
    print(f"{colors.bold}{string}{colors.endl}")

def takeIn(string):
    return input(f"{colors.bold}{string}{colors.endl}")

def placeItem(space):
    if space - 1 < 0 or space > 9:
        return False
    
    if space <= 3:
        if board[0][space-1] != colors.red + "X" + colors.endl and board[0][space-1] != colors.blue + "O" + colors.endl:
            board[0][space-1] = turn
        else:
            return False
    elif space <= 6:
        if board[1][space-4] != colors.red + "X" + colors.endl and board[1][space-4] != colors.blue + "O" + colors.endl:
            board[1][space-4] = turn
        else:
            return False
    elif space <= 9:
        if board[2][space-7] != colors.red + "X" + colors.endl and board[2][space-7] != colors.blue + "O" + colors.endl:
            board[2][space-7] = turn
        else:
            return False
        
    return True

def switchTurn(turn):
    if turn == colors.red + "X" + colors.endl:
        return colors.blue + "O" + colors.endl
    else:
        return colors.red + "X" + colors.endl
    
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
    if board[x][y] != colors.red + "X" + colors.endl and board[x][y] != colors.blue + "O" + colors.endl:
        return True
    else:
        return False

def minimax(board, depth, isMax):
    winner = checkWin(board)

    if winner != False:
        if winner == "draw":
            return 0
        else:
            if winner == colors.red + "X" + colors.endl:
                return -1
            else:
                return 1
            
    if isMax:
        bestScore = -1000
        for x in range(3):
            for y in range(3):
                if freeSpace(x, y, board):
                    prevName = board[x][y]
                    board[x][y] = colors.blue + "O" + colors.endl
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
                    board[x][y] = colors.red + "X" + colors.endl
                    score = minimax(board, depth+1, True)
                    board[x][y] = prevName
                    if score < bestScore:
                        bestScore = score
        
        return bestScore
    
def playerTurn():
    while True:
        try:
            selectedSpace = int(takeIn("Where would you like to go? "))
        except ValueError:
            os.system("clear")
            showBoard()
            output("Please select a different space...")
            continue
        
        if not placeItem(selectedSpace):
            os.system("clear")
            showBoard()
            output("Please select a different space...")
        else:
            break

def aiTurn():
    bestScore = -1000
    bestMove = [0, 0]
    for x in range(3):
        for y in range(3):
            if freeSpace(x, y, board):
                prevName = board[x][y]
                board[x][y] = colors.blue + "O" + colors.endl
                score = minimax(board, 0, False)
                board[x][y] = prevName
                if score > bestScore:
                    bestScore = score
                    bestMove = [x, y]
    
    board[bestMove[0]][bestMove[1]] = colors.blue + "O" + colors.endl

if __name__ == '__main__':
    os.system("clear")
    while True:
        global gameType
        gameType = takeIn("Player vs. Player (1)\nPlayer vs. AI. (2)\n\nChosen: ")
        if gameType == "1":
            gameType = "2p"
            break
        elif gameType == "2":
            gameType = "1p"
            break
        else:
            os.system("clear")
            output("Please select an allowed type...")

    while True:
        os.system("clear")
        showBoard()

        winner = checkWin(board)

        if winner != False:
            if winner == "draw":
                output("The game is tied")
                exit(0)
            else:
                output(f"'{winner}' has won the game")
                exit(0)

        if gameType == "2p":
            output(f"It is {turn}'s turn")
            playerTurn()
        else:
            if turn == colors.red + "X" + colors.endl:
                output(f"It is X's turn")
                playerTurn()
            else:
                output(f"It is O's turn")
                aiTurn()

        turn = switchTurn(turn)

