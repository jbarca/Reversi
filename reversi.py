'''
Author: Jacob Barca
'''

# Import necessary modules
import copy

def new_board():
	# Set up board list
	board = []
	# Create the 2D 8x8 matrix containing 8 lists of 8 0's
	for i in range(8):
		row = []
		for j in range(8):
			row.append(0)
		board.append(row)

	# Set the starting position conditions.
	board[3][3] = 2
	board[4][3] = 1
	board[3][4] = 1
	board[4][4] = 2

	# Return the current board state.
	return board

def print_board(board):
	# Create a deep copy of the board so the original board isn't changed.
	board_copy = copy.deepcopy(board)

	# Set the player piece to either 'B' or 'W' or ' '.
	for i in range(len(board_copy)):
		for j in range(len(board_copy[i])):
			if board_copy[i][j] == 0:
				board_copy[i][j] = " "
			elif board_copy[i][j] == 1:
				board_copy[i][j] = "B"
			elif board_copy[i][j] == 2:
				board_copy[i][j] = "W"

	# Format the board so it is readable.
	i = 0 
	j = 0
	count = 1
	while i < len(board_copy):
		print("\t-----"*len(board_copy))
		print(count, end="")
		j = 0
		while j < len(board_copy[i]):
			if j == 7:
				print(("\t| {0} |".format(board_copy[i][j])))
			else:
				print(("\t| {0} |".format(board_copy[i][j])), end="")
			j += 1
		i += 1
		count += 1
	print("\t-----"*len(board_copy))
	print("")
	print("\t  a       b       c       d       e       f       g       h")
	print("\n")

def score(board):
	# Set up player 1 and player 2's score variables
	p1_score = 0
	p2_score = 0

	# For each row in the board, append the 1's and 2's to 
	# player 1 and player 2's score variables respectively.
	for row in board:
		for num in row:
			if num == 1:
				p1_score += 1
			elif num == 2:
				p2_score += 1

	# Return player 1 and player 2's scores in a tuple.
	return (p1_score, p2_score)

'''
Directions:

Horizontal up: (-1, 0)
Horizontal down: (1, 0)
Horizontal left: (0, -1)
Horizontal right: (0, 1)
Diagonal up right: (-1, 1)
Diagonal down right: (1, 1)
Diagonal up left: (-1, -1)
Diagonal down left: (1, -1)
'''

def enclosing(board, player, pos, dir):
	# If the player = 1, the other player is set to 2.
	if player == 1:
		op = 2
	# Otherwise it is set to 1.
	else:
		op = 1
	# Check if the values of pos and dir are in their allowed ranges.
	if pos[0] in range(8) and pos[1] in range(8) and dir[0] in range(-1, 2) and dir[1] in range(-1, 2):
		# If the location on the board isn't already occupied.
		if (board[pos[0]][pos[1]] == 0):
			# Check if the next location in the direction is in the allowed range.
			if (pos[0]+dir[0] in range(8) and pos[1]+dir[1] in range(8)):
				# If the next location in the direction is the other player's stone,
				# set a list containing the current coordinates to this position.
				if (board[pos[0]+dir[0]][pos[1]+dir[1]] == op):
					current_pos = [pos[0]+dir[0], pos[1]+dir[1]]
					# While the current position of the board is not the current player's stone and 
					# is not empty, move to the next position in the direction.
					while (board[current_pos[0]][current_pos[1]] != player and board[current_pos[0]][current_pos[1]] != 0):
						# Check if the next position is in the allowed range.
						if (current_pos[0]+dir[0] in range(8) and current_pos[1]+dir[1] in range(8)):
							# Set the next position to the current position.
							current_pos[0] = current_pos[0] + dir[0]
							current_pos[1] = current_pos[1] + dir[1]
						# If the path goes out of the range, return False.
						else:
							return False
					# If a 0 is found along the path, it is not enclosed.
					if (board[current_pos[0]][current_pos[1]] == 0):
						return False
					# If the current player's piece successfully encloses the other player's pieces successively,
					# it is enclosed.
					else:
						return True
				# If the next location after the current player's piece is a 0, it cannot be enclosed.
				else:
					return False
			# If the next location is not in the allowed range, it cannot be enclosed.
			else:
				return False
		else:
			return False
	# If the user inputs a position or direction outside of the allowed range,
	# then we cannot enclose anything.
	else:
		return False

def flip_pos(board, player, pos, dir):
	# If the player = 1, the other player is set to 2.
	if player == 1:
		op = 2
	# Otherwise it is set to 1.
	else:
		op = 1
	# Sets up the positions to enclose in a given direction.
	pos_to_flip = []
	# Does everything enclosing() does except everytime it finds the other player's piece it 
	# adds the position of that piece to a list.
	current_pos = [pos[0]+dir[0], pos[1]+dir[1]]

	while (board[current_pos[0]][current_pos[1]] != player and board[current_pos[0]][current_pos[1]] != 0):
		if (board[current_pos[0]][current_pos[1]] == op):
			pos_to_flip.append((current_pos[0], current_pos[1]))

		if (current_pos[0]+dir[0] in range(8) and current_pos[1]+dir[1] in range(8)):
			current_pos[0] = current_pos[0] + dir[0]
			current_pos[1] = current_pos[1] + dir[1]

	# Returns all the positions to flip in a given direction.
	return pos_to_flip

def valid_moves(board, player):
	# Set up the list of valid board positions.
	board_positions = []

	# Loop through all the combinations of pos(i, j) and dir(k, l)
	# and check using the enclosing function if the positions are valid.
	for i in range(0, 8):
		for j in range(0, 8):
			for k in range(-1, 2):
				for l in range(-1, 2):
					# Checking the direction (0, 0) results in an infinite loop, so we 
					# pass over it.
					if ((k, l) == (0, 0)):
						continue
					else:
						# If a position is valid, append the positions in tuple format to the 
						# list.
						if (enclosing(board, player, (i, j), (k, l))):
							board_positions.append((i, j))

	# Return all the valid board positions for the player.
	return board_positions

def valid_directions(board, player, board_position):
	# Loops through all of the combinations of directions for a given board position
	# and returns ALL the directions that are valid in that given position.
	valid_dirs = []
	# For each combination of directions, loop through and if the direction is valid,
	# add it to a list of valid directions.
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (enclosing(board, player, (board_position[0], board_position[1]), (i, j))):
				valid_dirs.append((i, j))
	# Finally return the valid direction list.
	return valid_dirs

def next_state(board, player, pos):
	# If the player = 1, the other player is set to 2.
	if player == 1:
		op = 2
	# Otherwise it is set to 1.
	else:
		op = 1
	# Declares a copy of "board" such that there are no references to the original copy.
	# Hence, the copy.deepcopy.
	next_board = copy.deepcopy(board)
	next_player = 0

	# If there are any valid moves for the player, continue.
	if (len(valid_moves(board, player)) > 0):
		# Set the value of the valid board position to 1 or 2 for the current player.
		next_board[pos[0]][pos[1]] = player
		# Next it is the other player's turn.
		next_player = op
		# For each position in the positions to be flipped, set the value of that
		# position to 1, which is equivalent to flipping all of the enclosed pieces.

		# Search for ALL valid directions where pieces can be flipped, to enable
		# 2 or more directions to be flipped at the same time.
		for dirs in valid_directions(board, player, (pos[0], pos[1])):
			for position in flip_pos(board, player, pos, (dirs[0], dirs[1])):
				next_board[position[0]][position[1]] = player
		# Return the state of the next_board and the next player in a tuple pair.
		return (next_board, next_player)
	# If there are no valid moves for the player, return the original board
	# and 0 for the player. The game is over.
	else:
		return (next_board, next_player)

def position(string):
	# Create the lists to check for the row numbers and column letters
	row_nums = ['1', '2', '3', '4', '5', '6', '7', '8']
	column_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	# Check if the string input is in the valid format and is contained in the lists.
	if (len(string) == 2 and string[0] in column_letters and string[1] in row_nums):
		# For each letter in column_letters check if the first element ofthe string 
		# is equal to one of the letters in the list.
		for letter in column_letters:
			if string[0] == letter:
				# If it is equal, set the column variable equal to it's index.
				column = column_letters.index(letter)

		# For each number in the list of row numbers, check if the second element of the 
		# string is equal to one of the characters in the list.
		for num in row_nums:
			if string[1] == num:
				# If a character is equal, get it's index.
				row = row_nums.index(num)
		
		# Finally, return the row and column in a tuple pair.
		return (row, column)
	
	# If the input is garbage, return nothing.
	else:
		return None
	
def board_pos(pos):
	# Converts the AI's coordinates into a board position
	row_nums = ['1', '2', '3', '4', '5', '6', '7', '8']
	column_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

	board_position = column_letters[pos[1]] + row_nums[pos[0]]
	return board_position

def get_max_score_pos(board, player):
	# Setting up maximum score and maximum score position variables.
	max_score = 0
	max_score_pos = []

	# For each valid position for a given board position and player, 
	# if the score of the next state on the board after placing down a piece is greater
	# than the max_score, replace the max_score with that score.
	for vm in valid_moves(board, player):
		if score(next_state(board, player, (vm[0], vm[1]))[0])[player-1] > max_score:
			max_score = score(next_state(board, player, (vm[0], vm[1]))[0])[player-1]
			# Append the score and position to a list, to be sorted.
			max_score_pos.append((max_score, vm))
	# Sort the list with respect to the maximum score which is done by an anonymous 
	# function.
	best_pos = sorted(max_score_pos, key=lambda x: x[0])
	# Return the last element (which is the highest score in the sorted list) and the 
	# position at which the maximum score was obtained.
	return best_pos[-1][1]

def run_two_players():
	# Set up the new board and print it in human-readable format.
	board = new_board()
	print_board(board)
	# Set the player = 1 as black always goes first.
	player = 1
	# Ask the user for a board position.
	turn = input("Player " + str(player) + "'s move: ")
	# While the user doesnt enter "q" for quit, convert the string to a board position,
	# and check if it is in the list of valid moves.
	while turn != "q":
		# If the input from the user is within the range of board positions, continue.
		if (position(turn) != None):
			# If the length of the list of valid moves for the next board and next player is 
			# greater than 0, continue the game.
			if (len(valid_moves(next_state(board, player, position(turn))[0], next_state(board, player, position(turn))[1])) > 0):
				# If the position is in the list of valid moves, continue.
				if (position(turn) in valid_moves(board, player)):
					# Assign the 0'th and 1'st element to board and player respectively.
					# The 0'th element is the next board
					# The 1'st element is the next player
					board, player = next_state(board, player, position(turn))
					# Print the next board state.
					print_board(board)

					turn = input("Player " + str(player) + "'s move: ")
						
				# If board position does not contain any valid moves, let the user know
				# that it is an invalid move and ask for another board position to continue the 
				# game.
				else:
					print("Invalid move.")
					turn = input("Player " + str(player) + "'s move: ")
			# If there are no valid moves left, finish the game.
			else:
				# If both player 1 and player 2 have no more valid moves in the next board state,
				# end the game.
				if (len(valid_moves(next_state(board, player, position(turn))[0], 1)) == 0 and len(valid_moves(next_state(board, player, position(turn))[0], 2)) == 0):
					board = next_state(board, player, position(turn))[0]
					# Print the final board state
					print_board(board)
					# Display a game over message and the score
					print("Game over!")
					print("Score:", score(board)[0], "-", score(board)[1])

					# Calculate who won based on the score values.
					if score(board)[0] > score(board)[1]:
						print("Player 1 wins!")
					elif score(board)[0] == score(board)[1]:
						print("Draw!")
					else:
						print("Player 2 wins!")
					# Finally, exit the program.
					exit(0)
				# If one of the players has no valid moves, switch to the other player.
				else:
					if (position(turn) in valid_moves(board, player)):
						board = next_state(board, player, position(turn))[0]
						print_board(board)
						print("Player", next_state(board, player, position(turn))[1], "has no valid moves.")
						turn = input("Player " + str(player) + "'s move: ")
					else:
						print("Invalid move.")
						turn = input("Player " + str(player) + "'s move: ")
		# If the user's input is something else, display an invalid move message and
		# ask the user for another position.
		else:
			print("Invalid move.")
			turn = input("Player " + str(player) + "'s move: ")

def run_single_player():
	# Set up variables
	board = new_board()
	print_board(board)
	player = 1

	# Ask the user (player 1) for a board position.
	turn = input("Player " + str(player) + "'s move: ")
	# While the input is not equal to "q", continue.
	while turn != "q":
		# If the input is a valid board position, continue.
		if (position(turn) != None):
			# If the length of the list of valid moves for the next board and next player is 
			# greater than 0, continue the game.
			if (len(valid_moves(next_state(board, player, position(turn))[0], next_state(board, player, position(turn))[1])) > 0):
				# If it is player 1's turn, check if the position is valid,
				# set the next board state and player and print the board state.
				if (position(turn) in valid_moves(board, player)):
					board, player = next_state(board, player, position(turn))
					print_board(board)
					# If it is player 2's turn (AI), get the best position based on the score
					# and switch over to player 1.
					best_pos = get_max_score_pos(board, player)
					board, player = next_state(board, player, best_pos)

					print("Player 2's move:", board_pos(best_pos))

					print_board(board)
					# If player 1 has any valid moves, continue.
					if (len(valid_moves(board, player)) > 0):
						turn = input("Player " + str(player) + "'s move: ")
				# If the position isn't valid, display an invalid move message.
				else:
					print("Invalid move.")
					turn = input("Player " + str(player) + "'s move: ")

			# If there are no valid moves next for the next state, check which player has
			# no more valid moves.
			else:
				# If there are no valid positions for either player, end the game.
				if (len(valid_moves(next_state(board, player, position(turn))[0], 1)) == 0 and len(valid_moves(next_state(board, player, position(turn))[0], 2)) == 0):
					board = next_state(board, player, position(turn))[0]
					print_board(board)

					print("Game over!")
					print("Score:", score(board)[0], "-", score(board)[1])

					if score(board)[0] > score(board)[1]:
						print("Player 1 wins!")
					elif score(board)[0] == score(board)[1]:
						print("Draw!")
					else:
						print("Player 2 wins!")
					exit(0)
				
				else:
					# If player 1 has no more valid moves, switch to player 2 and perform the 
					# best position algorithm, then switch back to player 1.
					if (len(valid_moves(next_state(board, player, position(turn))[0], 1)) == 0):
							print_board(board)
							print("Player", player, "has no valid moves.")

							best_pos = get_max_score_pos(board, 2)
							board, player = next_state(board, 2, best_pos)

							print("Player 2's move:", board_pos(best_pos))

							print_board(board)

							if (len(valid_moves(board, player)) > 0):
								turn = input("Player " + str(player) + "'s move: ")

					# If player 2 has no more valid moves, switch to player 1 and ask them for another
					# position.
					elif (len(valid_moves(next_state(board, player, position(turn))[0], 2)) == 0):
						if (len(valid_moves(next_state(board, player, position(turn))[0], player)) > 0):
							if (position(turn) in valid_moves(board, player)):
								board = next_state(board, player, position(turn))[0]
								print_board(board)
								print("Player", next_state(board, player, position(turn))[1], "has no valid moves.")
								turn = input("Player " + str(player) + "'s move: ")
							else:
								print("Invalid move.")
								turn = input("Player " + str(player) + "'s move: ")
		# If the position is not in the list of valid positions, display an invalid move
		# message and ask for another position.
		else:
			print("Invalid move.")
			turn = input("Player " + str(player) + "'s move: ")

#run_single_player()
#run_two_players()

# Finished Task 2: Reversi (18 marks)
