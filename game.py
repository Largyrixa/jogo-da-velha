import os
from time import sleep
from random import choice, randint
import json

def main():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Display a colorful welcome animation
    for c in 'WELCOME TO TIC-TAC-TOE!':
        print(f'\033[1;{randint(31,36)}m{c}\033[m', end='')
        sleep(0.1)
    print('\n')
    
    # Player chooses their marker (X or O)
    player_marker = chooseMarker()
    bot_marker = 'X' if player_marker == 'O' else 'O'
    
    # Initialize an empty board
    board: list = [['' for _ in range(3)] for _ in range(3)]
    
    # Main game loop
    while checkWinner(board) == False:
        if player_marker == 'X':
            # Player X makes their move
            player_move = getMove(board)
            moveX, moveY = player_move
            board[moveX][moveY] = player_marker
            if checkWinner(board) != False:
                break
            # Bot makes its move
            bot_move = botMove(board, bot_marker)[0]
            moveX, moveY = bot_move
            board[moveX][moveY] = bot_marker
        else:
            # Bot makes its move
            bot_move = botMove(board, bot_marker)[0]
            moveX, moveY = bot_move
            board[moveX][moveY] = bot_marker
            if checkWinner(board) != False:
                break
            # Player O makes their move
            player_move = getMove(board)
            moveX, moveY = player_move
            board[moveX][moveY] = player_marker
    
    # Check the game result
    winner = checkWinner(board)
    
    # Show the final board with animation
    showBoardAnim(board)
    sleep(1)
    
    # Display win, lose, or draw message
    if winner == player_marker:
        winAnimation(board)
        for c in 'YOU WON!':
            print(f'\033[1;3{randint(1,6)}m{c}', end='')
            sleep(0.3)
        print('\033[m')
    elif winner == bot_marker:
        winAnimation(board)
        for c in 'YOU LOST!':
            print(f'\033[1;3{randint(1,6)}m{c}', end='')
            sleep(0.3)
        print('\033[m')
    else:
        drawAnimation(board)
        for c in 'IT\'S A TIE!':
            print(f'\033[1;3{randint(1,6)}m{c}', end='')
            sleep(0.3)
        print('\033[m')
    
    # Wait for user input to continue
    input('\nPress \033[32mENTER\033[m to continue...')

def chooseMarker():
    # Function for the player to choose their marker (X or O)
    while True:
        print('Choose a marker:\n[\033[1;31mX\033[m]\n[\033[1;34mO\033[m]')
        marker = input('\033[35m>>>\033[m').strip().upper()
        if marker not in ('X', 'O'):
            print('\033[1;31mCHOOSE ONLY AVAILABLE OPTIONS (X OR O)\033[m')
            continue
        return marker

def checkWinner(board):
    # Check if there is a winner or a tie
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != '' or board[0][2] == board[1][1] == board[2][0] != '':
        return board[1][1]
    
    for row in board:
        for el in row:
            if el == '':
                return False
    
    return 'tie'

def showBoard(board):
    # Display the current board
    os.system('cls' if os.name == 'nt' else 'clear')
    for l in range(3):
        for c in range(3):
            if c != 0:
                print('\033[1m|\033[m', end='')
            
            if board[l][c] == '':
                print('\033[1;33m'+f'{l} {c}'+'\033[m', end='')
            elif board[l][c] == 'X':
                print('\033[1;31m X \033[m', end='')
            elif board[l][c] == 'O':
                print('\033[1;34m O \033[m', end='')
        print()
        if l != 2:
            print('\033[1m---+---+---\033[m')

def getMove(board):
    # Get the player's move
    showBoard(board)
    entry = input('\033[1mChoose a coordinate\n\033[35m>>>\033[m').strip()
    move = []
    
    for char in entry:
        if char.isnumeric():
            move.append(int(char))
    
    while (output := isValidMove(board, move)) != True:
        print('\033[1;31m'+output+'\033[m')
        sleep(2)
        showBoard(board)
        entry = input('Choose a coordinate\n->').strip()
        move = []
        for char in entry:
            if char.isnumeric():
                move.append(int(char))
    
    return move

def isValidMove(board, move):
    # Validate if the move is valid
    print()
    if len(move) != 2:
        return "ONLY ENTER TWO NUMBERS AS SHOWN ON THE BOARD!"
    
    for x in move:
        if x not in range(3):
            return "ONLY ENTER COORDINATES PRESENT ON THE BOARD!"
    
    jx, jy = move
    if board[jx][jy] != '':
        return "THIS SPOT HAS ALREADY BEEN CHOSEN!"
    
    return True

def makeStrBoard(board):
    strBoard = ''
    for row in board:
        for el in row:
            if el == '':
                strBoard += ' '
            else:
                strBoard += el
    return strBoard 

def backtracking(board, marker):
    # Backtracking algorithm to determine the bot's best move
    winner = checkWinner(board)
    if winner == False:
        output = botMove(board, 'X' if marker == 'O' else 'O')[1]
        return output * (-1)
    
    if winner == marker:
        return 1
    elif winner == 'tie':
        return 0
    else:
        return -1

def botMove(board, marker):
    if useData == 'Y':
        try:
            response = choice(responses[marker][makeStrBoard(board)])
            return (response,0)
        except KeyError:
            pass
    
    # Determine the bot's move using backtracking
    valid_moves = list()
    temp_board = [row[:] for row in board]
    for x in range(3):
        for y in range(3):
            if temp_board[x][y] == '':
                valid_moves.append((x, y))
    results = []
    
    while len(valid_moves) != 0:
        move = choice(valid_moves)
        x, y = move
        temp_board[x][y] = marker
        results.append((move, backtracking(temp_board, marker)))
        temp_board[x][y] = ''
        for i, p in enumerate(valid_moves):
            if p == move:
                valid_moves.pop(i)
    
    # Choose the best move based on results
    wins = []
    ties = []
    losses = []
    for result in results:
        if result[1] == 1:
            wins.append(result)
        elif result[1] == 0:
            ties.append(result)
        else:
            losses.append(result)
    
    if len(wins) >= 1:
        return wins[0]
    elif len(ties) >= 1:
        return ties[0]
    else:
        return losses[0]

# Animation functions
def showBoardAnim(board):
    # Display the board with animation
    os.system('cls' if os.name == 'nt' else 'clear')
    for l in range(3):
        for c in range(3):
            if c != 0:
                print('\033[1m|\033[m', end='')
            
            if board[l][c] == '':
                print('   ', end='')
            elif board[l][c] == 'X':
                print('\033[1;31m X \033[m', end='')
            elif board[l][c] == 'O':
                print('\033[1;34m O \033[m', end='')
            else:
                print(f' {board[l][c]} ', end='')
        print()
        if l != 2:
            print('\033[1m---+---+---\033[m')

def winAnimation(board):
    # Win animation
    winner = checkWinner(board)
    for i, row in enumerate(board):
        if row[0] == row[1] == row[2] == winner:
            board[i] = [f'\033[32m{winner}\033[m' for _ in range(3)]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] == winner:
            for x in range(3):
                board[x][i] = f'\033[32m{winner}\033[m'
    if board[0][0] == board[1][1] == board[2][2] == winner:
        for x in range(3):
            board[x][x] = f'\033[32m{winner}\033[m'
    if board[0][2] == board[1][1] == board[2][0] == winner:
        for x in range(3):
            board[2 - x][x] = f'\033[32m{winner}\033[m'
    
    for _ in range(3):
        sleep(0.7)
        showBoardAnim(board)
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    showBoardAnim(board)

def drawAnimation(board):
    # Draw animation
    spots = []
    while len(spots) != 9:
        x, y = randint(0, 2), randint(0, 2)
        if (x, y) not in spots:
            spots.append((x, y))
    for _ in range(9):
        x, y = spots[len(spots) - 1]
        board[x][y] = f'\033[1;33m{board[x][y]}\033[m'
        spots.pop()
        sleep(0.5)
        showBoardAnim(board)

def loadResponses():
    # Load saved responses from the JSON file
    with open('responses.json') as file:
        return json.load(file)

def saveResponses():
    # Save responses to the JSON file
    with open('responses.json', 'w') as file:
        json.dump(responses, file)

def addResponse(response, board, marker):
    # Add a response to the responses dictionary
    str_board = ''
    response = response
    for row in board:
        for spot in row:
            if spot == '':
                str_board += ' '
            else:
                str_board += spot
    new = True
    for game, possibilities in responses[marker].items():
        if game == str_board:
            if response not in possibilities:
                responses[marker][str_board].append(response)
            new = False
            break
    if new:
        responses[marker][str_board] = [response]

if __name__ == '__main__':
    responses: dict = loadResponses()
    useData = input("Do you want to use the Bot's databank (responses.json) in its responses? (Y/N)\n\033[35m>>>\033[m").strip().upper()
    while useData not in ('Y','N'):
        print('\033[1;31mCHOOSE ONLY BETWEEN Y AND N!\033[m')
        useData = input("Do you want to use the Bot's databank (responses.json) in its responses? (Y/N)\n\033[35m>>>\033[m").strip().upper()
    
    main()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        answer = input('\nWant to play again?(Y/N)\n\033[35m>>>\033[m').strip().upper()
        if answer not in ('Y', 'N'):
            print('\n\033[1;31mCHOOSE ONLY YES (Y) OR NO (N)!\033[m')
            continue
        if answer == 'Y':
            main()
        else:
            for c in 'GOODBYE!':
                print(f'\033[1;{randint(31,36)}m{c}\033[m', end='')
                sleep(0.2)
            exit()
