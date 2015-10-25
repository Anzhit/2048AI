import random     
import copy
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
def merge(nums,x):
    size = len(nums)
  # remove all the zeroes
    nums[:] = (value for value in nums if value != 0)
  # now do the merging, use an index to run through the list
    i = 0
    while (i < len(nums)-1 ):
        if (nums[i]==nums[i+1]): # if a number is the same as the following
            nums[i] *= 2           # double it 
            del nums[i+1]          # remove the following
            x.score+=nums[i]         # Increment Score
        i += 1
  # restore the initial list length appending zeroes
    while (len(nums) < size):
        nums.append(0)
  # done
    return nums

class TwentyFortyEight:
    # Class to run the game logic.

    def __init__(self, grid_height, grid_width):
        # Initialize class
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.cells = []
        self.reset()
        self.score=0

		# Compute inital row dictionary to make move code cleaner
        self.initial = {
			UP : [[0,element] for element in range(self.get_grid_width())],
			DOWN : [[self.get_grid_height() - 1, element] for element in range(self.get_grid_width())],
			LEFT : [[element, 0] for element in range(self.get_grid_height())],
			RIGHT : [[element, self.get_grid_width() - 1] for element in range (self.get_grid_height())]
		}
		
    def reset(self):
        # Reset the game so the grid is empty.
        self.cells = [[0 for col in range(self.get_grid_height())] for row in range(self.get_grid_width())]
        
    def __str__(self):
        # Print a string representation of the grid for debugging.
        for number in range(0, self.get_grid_height()):
            for x in range(self.grid_width):
                print(str(self.cells[number][x]) +"\t"),
            print
    
    def get_grid_height(self):
        # Get the height of the board.
        return self.grid_height
    
    def get_grid_width(self):
        # Get the width of the board.
        return self.grid_width

    def maxValue(self):
        """
        return the max value in the board
        """
        maxVal = 0
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                maxVal = max(self.get_tile(x,y),maxVal)
        return maxVal

    def canMove(self):
        """
        test if a move is possible
        """
        if(len(self.get_available_moves())):
            return True
        return False

    def move(self, direction):
        # Move all tiles in the given direction and add
        # a new tile if any tiles moved.
		initial_list = self.initial[direction]
		temporary_list = []

		if(direction == UP):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_height())
		elif(direction == DOWN):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_height())
		elif(direction == LEFT):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_width())
		elif(direction == RIGHT):
			self.move_helper(initial_list, direction, temporary_list, self.get_grid_width())

    def valid_move(self,direction):
        tmp=copy.deepcopy(self)
        tmp.move(direction)
        if(tmp.__dict__==self.__dict__):
            return False
        return True


    def move_helper(self, initial_list, direction, temporary_list, row_or_column):
		# Move all columns and merge
		before_move = str(self.cells)

		for element in initial_list:
			temporary_list.append(element)
			
			for index in range(1, row_or_column):
				temporary_list.append([x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])
			
			indices = []
			
			for index in temporary_list:
				indices.append(self.get_tile(index[0], index[1]))
			
			merged_list = merge(indices,self)
			
			for index_x, index_y in zip(merged_list, temporary_list):
				self.set_tile(index_y[0], index_y[1], index_x)
		
			temporary_list = []
		
		after_move = str(self.cells)
		
		if before_move != after_move:
			self.new_tile()	

    def new_tile(self):
        # Create a new tile in a randomly selected empty 
        # square.  The tile should be 2 90% of the time and
        # 4 10% of the time.
        available_positions = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] == 0:
                    available_positions.append([row, col])
 
        if not available_positions:
            print "There are no available positions."
        else:
            random_tile = random.choice(available_positions)
 
            weighted_choices = [(2, 9), (4, 1)]
            population = [val for val, cnt in weighted_choices for i in range(cnt)]
            tile = random.choice(population)

            self.set_tile(random_tile[0],random_tile[1], tile)

    def get_available_moves(self):
        return filter(self.valid_move,[1,2,3,4])
    def get_available_rand_moves(self):
        available_positions = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] == 0:
                    available_positions.append([row, col,2])
                    available_positions.append([row, col,4])
        return available_positions
    def set_tile(self, row, col, value):
        # Set the tile at position row, col to have the given value.
        self.cells[row][col] = value
            
    def get_tile(self, row, col):
        # Return the value of the tile at position row, col.
        return self.cells[row][col]
    def next_state(self,direction):
        tmp=copy.deepcopy(self)
        tmp.move(direction)
        return tmp
    def next_state_random(self,l):
        tmp=copy.deepcopy(self)
        tmp.set_tile(l[0],l[1],l[2])
        return tmp
    def evaluate(self):
        return self.maxValue()*self.score
    def isfilled(self):
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if(self.cells[x][y]==0):
                    return False
        return True
def minimax_alpha_beta(game_state,depth):

  return max(
    map(lambda move: (move, ABmin_play(game_state.next_state(move),-float('inf'),float('inf'),depth)), 
      game_state.get_available_moves()), 
    key = lambda x: x[1])[0]

def ABmin_play(game_state,alpha,beta,depth):
    if game_state.isfilled() or depth==0:
        return game_state.evaluate()
    v = float('inf')
    for move in game_state.get_available_rand_moves():
        s=game_state.next_state_random(move)
        v = min(v, ABmax_play(s, alpha, beta, depth-1))
        if v <= alpha:
            return v
        alpha = min(beta, v)
    return v

def ABmax_play(game_state,alpha,beta,depth):
    if not(game_state.canMove()) or depth==0:
        return game_state.evaluate()
    
    v = -float('inf')
    for move in game_state.get_available_moves():
        s=game_state.next_state(move)
        v = max(v, ABmin_play(s, alpha, beta, depth-1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v
def minimax(game_state,depth):

  return max(
    map(lambda move: (move, min_play(game_state.next_state(move),depth)), 
      game_state.get_available_moves()), 
    key = lambda x: x[1])[0]

def min_play(game_state,depth):
  if game_state.isfilled() or depth==0:
    return game_state.evaluate()
  return min(
    map(lambda move: max_play(game_state.next_state_random(move),depth-1),
      game_state.get_available_rand_moves()))

def max_play(game_state,depth):
  if not(game_state.canMove()) or depth==0:
    return game_state.evaluate()
  return max(
    map(lambda move: min_play(game_state.next_state(move),depth-1),
      game_state.get_available_moves()))
x=TwentyFortyEight(4,4)
x.new_tile()
while(x.canMove()):
    x.__str__()
    print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
    dir=minimax_alpha_beta(x,5)
    print(dir)
    x.move(dir)