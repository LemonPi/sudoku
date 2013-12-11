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
    print("s: save, q: quit")

    # Requesting moves from players
    while make_move('A') and make_move('B'):  
    	pass

    #  TODO

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
                save_name = input("Enter file name: ")
                try:  # see if file exists already
                    with open(save_name):
                        process()  # try to process file
                        confirm = input("File exists, override(Y)?: ")
                        if confirm in ['Y','y','yes','yup','sure','of course']:
                            with open(save_name,'w') as save:
                                save = show(save)
                except IOError:  # if file doesn't exist
                    try:  # in case we do not have permission to write to file
                        with open(save_name,'w') as save:
                            save = show(save)
                    except OSError:
                        print("Can't write to that file!")
                        pass

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
           	       print("s: save, q: quit")
           	       return True  # exits loop and function
               else:
                   print("Does not pass into check_move")
        except:  # in case user_input does not have 3 elements
            continue

def check_move(row, col, val):
    """
    (int(row), int(col), int(val)) -> bool
    Return true if move is valid: the value does not exist in the row,
    column, and sector that it is in and does not erase an existing value.
    """
   
    if board[row][col]:  # if the board at [row][col] is not 0
    	print("element exists")
    	return False
    for row_element in board[row]:  # check duplicate in row
    	if val == row_element:
    		print("Duplicate in row")
    		return False
    for row_n in board:  # check duplicate in col
    	if val == row_n[col]:
    		print("Duplicate in col")
    		return False
    # use int divide to check quadrant
    cluster_s = int(len(board) ** (1/2))  # cluster size
    row_clus = row // cluster_s  
    col_clus = col // cluster_s
    for r in range(cluster_s):  # cluster will be cluster_s by cluster_s in size
    	for c in range(cluster_s):
            # row_clus * cluster_s provides starting point for cluster
    		if board[r + row_clus*cluster_s][c + col_clus*cluster_s] == val:
    			print("Duplicate in cluster")
    			return False
    return True  # if all other passed

import sys
def show(save = sys.stdout):  # allows this function to save as well as show
    """
    (str(save)) -> no return
    Print the current board to file specified; default is stdout.
    """
    cluster_s = int(len(board) ** (1/2))
    for r in range(len(board)):
        # need r not be first or last and is a multiple of cluster_s
        if r != 0 and r != len(board) - 1 and not r % cluster_s:
            print("{}".format('-' * len(board) * 2), file = save)
        for c in range(len(board[0])):
            if c != 0 and c != len(board) - 1 and not c % cluster_s:
                print("|", end = '', file = save)
            elif c != 0:  # starting columns do not need space prepended
                print(" ", end = '', file = save)
            print(board[r][c], end = '', file = save)
        print(file = save)  # line break between rows


if __name__ == "__main__":
	play()
