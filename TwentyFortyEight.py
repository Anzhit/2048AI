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
initial={
			UP : [[0,element] for element in range(4)],
			DOWN : [[4 - 1, element] for element in range(4)],
			LEFT : [[element, 0] for element in range(4)],
			RIGHT : [[element, 4 - 1] for element in range (4)]
		}
grid_height=4
grid_width=4
class TwentyFortyEight:
	# Class to run the game logic.

	def __init__(self):
		# Initialize class
		self.cells = 0;
		self.score=0
		
	def __str__(self):
		# Print a string representation of the grid for debugging.
		global grid_width
		global grid_height
		for number in range(grid_height):
			for x in range(grid_width):
				print(str(1<<self.get_tile(number, x)) +"\t",end=" ")
			print("",end="\n")

	def get_grid_height(self):
		# Get the height of the board.
		global grid_height
		return grid_height
	
	def get_grid_width(self):
		# Get the width of the board.
		global grid_width
		return grid_width

	def maxValue(self):
		"""
		return the max value in the board
		"""
		maxVal = 0
		global grid_width
		global grid_height
		for y in range(grid_height):
			for x in range(grid_width):
				maxVal = max(self.get_tile(x,y),maxVal)
		return 1<<maxVal

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
		global initial
		initial_list = initial[direction]

		if(direction == UP):
			self.move_helper(initial_list, direction, self.get_grid_height())
		elif(direction == DOWN):
			self.move_helper(initial_list, direction, self.get_grid_height())
		elif(direction == LEFT):
			self.move_helper(initial_list, direction, self.get_grid_width())
		elif(direction == RIGHT):
			self.move_helper(initial_list, direction,  self.get_grid_width())

	def valid_move(self,direction):
		tmp = TwentyFortyEight()
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.move(direction)
		if(tmp.cells==self.cells):
			return False
		return True


	def move_helper(self, initial_list, direction, row_or_column):
		# Move all columns and merge
		before_move = self.cells
		temporary_list = []
		for element in initial_list:
			temporary_list.append(element)
			
			for index in range(1, row_or_column):
				temporary_list.append([x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])
			
			indices = [self.get_tile(index[0], index[1]) for index in temporary_list]
			
			merged_list = self.merge(indices)
			
			for index_x, index_y in zip(merged_list, temporary_list):
				self.set_tile(index_y[0], index_y[1], index_x)
		
			temporary_list = []
		
		after_move = self.cells

		if before_move != after_move:
			self.new_tile()	

	def new_tile(self):
		# Create a new tile in a randomly selected empty 
		# square.  The tile should be 2 90% of the time and
		# 4 10% of the time.
		available_positions = []
		global grid_width
		global grid_height
		for row in range(grid_height):
			for col in range(grid_width):
				if self.get_tile(row, col) == 0:
					available_positions.append([row, col])
 
		if not available_positions:
			print("There are no available positions.")
		else:
			random_tile = random.choice(available_positions)
 
			weighted_choices = [(1, 9), (2, 1)]
			population = [val for val, cnt in weighted_choices for i in range(cnt)]
			tile = random.choice(population)

			self.set_tile(random_tile[0],random_tile[1], tile)

	def get_available_moves(self):
		return list(filter(self.valid_move,[1,2,3,4]))

	def get_available_rand_moves(self):
		global grid_width
		global grid_height
		available_positions = []
		for row in range(grid_height):
			for col in range(grid_width):
				if self.get_tile(row, col) == 0:
					available_positions.append([row, col,2])
					available_positions.append([row, col,4])
		return available_positions

	def set_tile(self, row, col, value):
		# Set the tile at position row, col to have the given value.
		global grid_width
		global grid_height
		x = 15 << 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1)
		self.cells = self.cells | x

		y = 0xffffffffffffffff
		value1 = 15 - value
		y = y - (value1 << 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1))
		self.cells = self.cells & y
				
	def get_tile(self, row, col):
		# Return the value of the tile at position row, col.
		global grid_width
		global grid_height
		x = 15 << 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1)
		x = self.cells & x
		x = x >> 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1)
		return x

	def next_state(self,direction):
		tmp = TwentyFortyEight()
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.move(direction)
		return tmp

	def next_state_random(self,l):
		tmp = TwentyFortyEight()
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.set_tile(l[0],l[1],l[2])
		return tmp

	def evaluate(self):
		return self.maxValue()*self.score

	def isfilled(self):
		global grid_width
		global grid_height
		for x in range(grid_height):
			for y in range(grid_width):
				if(self.get_tile(x, y)==0):
					return False
		return True

	def merge(self, nums):
		size = len(nums)
	  # remove all the zeroes
		nums[:] = (value for value in nums if value != 0)
	  # now do the merging, use an index to run through the list
		i = 0
		while (i < len(nums)-1 ):
			if (nums[i]==nums[i+1]): # if a number is the same as the following
				nums[i] += 1           # double it 
				del nums[i+1]          # remove the following
				self.score+=1<<nums[i]         # Increment Score
			i += 1
	  # restore the initial list length appending zeroes
		while (len(nums) < size):
			nums.append(0)
	  # done
		return nums