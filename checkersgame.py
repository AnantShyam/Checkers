import random

def create_board():
    board = []
    for i in range(0, 8):
        if i == 0 or i == 2:
            board.append(['x' , ' '] * 4)
        elif i == 1:
            board.append([' ' , 'x'] * 4)
        elif i < 5:
            board.append([' '] * 8)
        elif i == 6 or i == 8:
            board.append(['o' , ' '] * 4)
        else:
            board.append([' ' , 'o'] * 4)

    return board

def display_board(board):
    #print([str(i) for i in range(len(board))])
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    print([i for i in letters])
    for i in range(len(board)):
        print(board[i], end= ' ')
        print([str(8 - i)])

def isInBounds(pos):
    return pos[0] >= 0 and pos[0] <=7 and pos[1] >= 0 and pos[1] <= 7

def isLegalStep(board, init, fin, player1, isKing, numsteps = 1):

    dist_y = fin[0] - init[0]
    dist_x = fin[1] - init[1]
    space_empty = board[fin[0]][fin[1]] == ' '
    inBounds = isInBounds(fin) and isInBounds(init)

    if player1:
        if isKing:
            dists_ok = abs(dist_y) == numsteps and abs(dist_x) == numsteps
            return space_empty and dists_ok and inBounds
        else:
            dists_ok = dist_y == -numsteps and abs(dist_x) == numsteps
            return space_empty and dists_ok and inBounds
    else:
        if isKing:
            dists_ok = abs(dist_y) == numsteps and abs(dist_x) == numsteps
            return space_empty and dists_ok and inBounds
        else:
            dists_ok = dist_y == numsteps and abs(dist_x) == numsteps
            return space_empty and dists_ok and inBounds

def isLegalJump(board, init, fin, isPlayer1):
    #fix bug here
    dist_y = fin[0] - init[0]
    dist_x = fin[1] - init[1]
    mid_y = int((init[0] + fin[0])/2)
    mid_x = int((init[1] + fin[1])/2)
    spaces_ok = False
    dists_ok = abs(dist_y) == 2 and abs(dist_x) == 2
    if isPlayer1:
        spaces_ok = board[init[0]][init[1]] in ['O', 'o'] and board[mid_y][mid_x] in ['X', 'x'] and board[fin[0]][fin[1]] == ' '
    else:
        spaces_ok = board[init[0]][init[1]] in ['X', 'x'] and board[mid_y][mid_x] in ['O', 'o'] and board[fin[0]][fin[1]] == ' '
    return isInBounds(init) and isInBounds(fin) and dists_ok and spaces_ok


def jumpExists(board, isPlayer1):

    jmp_pos = []
    poss_jmp_pos = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if isPlayer1:
                if board[i][j] == 'O':
                    poss_jmp_pos = [(i + 2, j - 2), (i + 2, j + 2), (i - 2, j - 2), (i - 2, j + 2)]

                elif board[i][j] == 'o':
                    poss_jmp_pos = [(i - 2, j - 2), (i - 2, j + 2)]
            else:
                if board[i][j] == 'X':
                    poss_jmp_pos = [(i + 2, j - 2), (i + 2, j + 2), (i - 2, j - 2), (i - 2, j + 2)]
                elif board[i][j] == 'x':
                    poss_jmp_pos = [(i + 2, j - 2), (i + 2, j + 2)]
            for pos in poss_jmp_pos:
                if isInBounds(pos) and isLegalJump(board, (i, j), pos, isPlayer1):
                    jmp_pos.append(pos)
    return [len(jmp_pos) != 0, jmp_pos]

                

def step(board, init, fin, isPlayer1, isKing, numsteps = 1):
    if isLegalStep(board, init, fin, isPlayer1, isKing, numsteps):
        if isPlayer1:
            if isKing:
                board[fin[0]][fin[1]] = 'O'
            else:
                if fin[0] == 0:
                    board[fin[0]][fin[1]] = 'O'
                else:
                    board[fin[0]][fin[1]] = 'o'
        else:
            if isKing:
                board[fin[0]][fin[1]] = 'X'
            else:
                if fin[0] == 7:
                    board[fin[0]][fin[1]] = 'X'
                else:
                    board[fin[0]][fin[1]] = 'x'

        board[init[0]][init[1]] = ' ' 

    if numsteps == 2:
        mid_y = int((init[0] + fin[0])/2)
        mid_x = int((init[1] + fin[1])/2)
        board[mid_y][mid_x] = ' '


def jump(board, init, fin, isPlayer1, isKing):
    if isLegalJump(board, init, fin, isPlayer1):
        if isLegalStep(board, init, fin, isPlayer1, isKing, 2):
            step(board, init, fin, isPlayer1, isKing, 2)


def number_of_o(board):
    count = 0
    for i in board:
        for j in i:
            if j in ['o', 'O']:
                count = count + 1
    return count

def number_of_x(board):
    count = 0
    for i in board:
        for j in i:
            if j in ['x', 'X']:
                count = count + 1
    return count

def parse_user_input(init, fin):
    interpreted_points = []
    cols = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H':7}
    for point in [init, fin]:
        xpos = cols[point[0]]
        ypos = 8 - int(point[1])
        interpreted_points.append((ypos, xpos))
    return interpreted_points


def play_checkers():
    print("Welcome to Checkers! To play this game on the command line, please note the following: ")
    print()
    print("A king is represented by a capital letter. ")
    print()
    print("Please enter the square you are either on or want to move to as for instance: D3.")

    print()
    print("Enjoy the game, and good luck!")
    print()

    player1 = str(input("What's your name, Player 1?:  "))
    player2 = str(input("What's your name, Player 2?:  "))
    print()
    board = create_board()
    display_board(board)       

    players = [player1, player2]
    pieces = [['o', 'O'], ['x', 'X']]
    idx = 0

    while number_of_o(board) != 0 and number_of_x(board) != 0:

        loopcontinue = True

        while loopcontinue:
            isPlayer1 = idx == 0

            try:
                player_input_init = input(players[idx] + ", please enter the current position of the piece you want to move: ")
                player_input_fin = input(players[idx] + ", please enter the final position of the piece you want to move: ")

                poslist = parse_user_input(player_input_init, player_input_fin)

                player_initpos = poslist[0]
                player_finpos = poslist[1]

                isKing = board[player_initpos[0]][player_initpos[1]] in ['O', 'X']
                if jumpExists(board, isPlayer1)[0]:
                    if player_finpos in jumpExists(board, isPlayer1)[1]:
                        midpty = int((player_initpos[0] + player_finpos[0])/2)
                        midptx = int((player_initpos[1] + player_finpos[1])/2)

                        if board[midpty][midptx] in pieces[1 - idx]:
                            jump(board, player_initpos, player_finpos, isPlayer1, isKing)

                            display_board(board)
                            idx = 1 - idx
                            loopcontinue = False
                        else:
                            print("You must jump!")
                            raise Exception()
                    else:
                        print("You must jump!")
                        raise Exception()
                elif isLegalStep(board, player_initpos, player_finpos, isPlayer1, isKing):
                    step(board, player_initpos, player_finpos, isPlayer1, isKing)
                    display_board(board)
                    idx = 1 - idx
                    loopcontinue = False
                else:
                    raise Exception()

            except:
                print()
                print("Sorry, invalid positions!")
                print()

    if number_of_o(board) == 0:
        print("Congratulations, " + players[1] + " you win!")
    else:
        print("Congratulations, " + players[0] + " you win!")
        
play_checkers()


