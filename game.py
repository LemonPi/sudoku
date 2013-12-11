def play():
    """
    () -> no return
    Execute body of the sudoku game.
    """

    # Setting the size of board
    N_valid = False
    while not N_valid:
        N = input("Enter size of grid N: ")
        if N in ['4','9','16']:
            N_valid = True
            N = int(N)
            global board  # make board accessible to all functions
            board = [[0 for x in range(N)] for x in range(N)]  # generates board
        else:
            print("You have entered an invalid grid size!")
    show()
    print("s: save, q: quit, l: load")

    # Requesting moves from players
    while True:
        num_moves = 0  # use number of movese to tell whose turn it is
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] != 0:
                    num_moves += 1

        if not num_moves % 2:  # 0 means even number, indicating A's move
            if make_move('A'):
                if check_win() == 2:
                    print("It's a tie!")
                    break
                elif check_win():
                    print("Player A has won!")
                    break
            else:
                break
        else:
            if make_move('B'):
                if check_win() == 2:
                    print("It's a tie!")
                    break
                elif check_win():
                    print("Player B has won!")
                    break
            else:
                break  # returns

def check_win():
    """
    () -> int
    Return if the last move won.
    """
    win = 0
    empty_spots = 0
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:  # check only if empty spot
                empty_spots += 1
                for val in range(1,len(board)):
                    win += check_move(r, c, val)  # increment for valid move
    if empty_spots == 0:  # if matrix is full
        return 2
    return not win  # if win == 0 then there are no valid moves, meaning they won

import os
def save():
    """
    () -> no return
    Saves state of game to a specified file.
    """
    save_name = input("Enter file name: ")
    if os.path.exists(save_name):
        confirm = input("File exists, override(Y)?: ")
        if confirm in ['Y','y','yes','yup','sure','of course']:
            with open(save_name, 'w') as save:
                save = show(save)
    else:
        try:  # in case we do not have permission to write
            with open(save_name,'w') as save:
                save = show(save)
        except OSError:
            print("Can't write to that file!")

def load():
    """
    () -> no return
    Loads game status from a saved file.
    """
    global board
    board = []  # reset board to prepare for appending
    line_n = 1
    load_name = input("Enter name of file to load: ")
    if os.path.exists(load_name):
        with open(load_name, 'r') as load:
            for line in load:
                if line[0] == '-':
                    continue
                line = line.replace('|',' ')
                line = line.split()  # kills both single and double spaces
                line = [int(val) for val in line]
                board.append(line)
    else:
        print("File does not exist")

def make_move(player):
    """
    (str(player)) -> bool
    Let player (A or B) make a move and updates the board.
    Return bool for whether play is continued.
    """
    global board
    valid_coord = [str(x) for x in range(len(board))]  # 0, 1, 2, ... N - 1
    valid_value = [str(x + 1) for x in range(len(board))]  # 1, 2, ... N
    while True:
        try:
            user_input = input("Player {} enter a move:".format(player))
            if user_input == 'q':
                return False
            if user_input == 's':
                save()
            if user_input == 'l':
                load()
                try:
                    show()
                    print("s: save, q: quit, l: load")
                    if check_win() == 2:
                        print("The loaded board is a tie!")
                        break
                except:
                    pass  # means the file trying to load does not exist
                return True  # return to play() after loading

            user_input = user_input.split(',')  # turn into list of fields
            for i in range(len(user_input)):
                user_input[i] = user_input[i].strip()  # remove whitespace 
            if (user_input[0] in valid_coord) and (user_input[1] in valid_coord) and\
               (user_input[2] in valid_value):  # first checks that entries are valid
               row = int(user_input[0])
               col = int(user_input[1])
               val = int(user_input[2])
               if check_move(row, col, val):
                      board[row][col] = val
                      show()
                      print("s: save, q: quit, l: load")
                      return True  # exits loop and function
        except OSError:  # in case user_input does not have 3 elements
            continue

def check_move(row, col, val):
    """
    (int(row), int(col), int(val)) -> bool
    Return true if move is valid: the value does not exist in the row,
    column, and sector that it is in and does not erase an existing value.
    """
    if board[row][col]:  # if element exists at row col
        return False
    for row_element in board[row]:  # check duplicate in row
        if val == row_element:
            return False
    for row_n in board:  # check duplicate in col
        if val == row_n[col]:
            return False
    # use int divide to check quadrant
    cluster_s = int(len(board) ** (1/2))  # cluster size
    row_clus = row // cluster_s  
    col_clus = col // cluster_s
    for r in range(cluster_s):  # cluster will be cluster_s by cluster_s in size
        for c in range(cluster_s):
            # row_clus * cluster_s provides starting point for cluster
            if board[r + row_clus*cluster_s][c + col_clus*cluster_s] == val:
                return False
    return True  # if all other passed

import math
import sys
def show(save = sys.stdout):  # allows this function to save as well as show
    """
    (str(save)) -> no return
    Print the current board to file specified; default is stdout.
    """
    digit_number = int(math.log(len(board)))  # change number of spacing
    cluster_s = int(len(board) ** (1/2))
    for r in range(len(board)):
        # need r not be first or last and is a multiple of cluster_s
        if r != 0 and r != len(board) - 1 and not r % cluster_s:
            # - for each element and space as well as extra space with >1 digit
            print('-' * (len(board) * 2 - 1 + \
                  len(board) * (digit_number - 1)) , file = save)  # extra spaces
        for c in range(len(board[0])):
            if c != 0 and c != len(board) - 1 and not c % cluster_s:
                print("|", end = '', file = save)
            elif c != 0:  # starting columns do not need space prepended
                print(' ', end = '', file = save)

            # dynamic alignment to make the board pretty
            print('{0:{fill}{align}{width}}'.format(board[r][c], fill = " ", 
            align = ">", width = digit_number), end = '', sep = '', file = save)
        print(file = save)  # line break between rows

if __name__ == "__main__":
    play()
