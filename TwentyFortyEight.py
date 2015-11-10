import random     
import copy

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Heuristic scoring settings
SCORE_LOST_PENALTY = 200000.0
SCORE_MONOTONICITY_POWER = 4.0
SCORE_MONOTONICITY_WEIGHT = 47.0
SCORE_SUM_POWER = 3.5
SCORE_SUM_WEIGHT = 11.0
SCORE_MERGES_WEIGHT = 700.0
SCORE_EMPTY_WEIGHT = 270.0

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
		   DOWN: (-1, 0), 
		   LEFT: (0, 1), 
		   RIGHT: (0, -1)} 

class TwentyFortyEight:
	# Class to run the game logic.

	def __init__(self, grid_height, grid_width):
		# Initialize class
		self.grid_height = grid_height
		self.grid_width = grid_width
		self.cells = 0;
		self.score=0

		# Compute inital row dictionary to make move code cleaner
		self.initial = {
			UP : [[0,element] for element in range(self.get_grid_width())],
			DOWN : [[self.get_grid_height() - 1, element] for element in range(self.get_grid_width())],
			LEFT : [[element, 0] for element in range(self.get_grid_height())],
			RIGHT : [[element, self.get_grid_width() - 1] for element in range (self.get_grid_height())]
		}
		
	def __str__(self):
		# Print a string representation of the grid for debugging.
		for number in range(0, self.get_grid_height()):
			for x in range(self.grid_width):
				print(str(1<<self.get_tile(number, x)) +"\t"),
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
		tmp = TwentyFortyEight(4, 4)
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.move(direction)
		if(tmp.cells==self.cells):
			return False
		return True


	def move_helper(self, initial_list, direction, temporary_list, row_or_column):
		# Move all columns and merge
		before_move = self.cells

		for element in initial_list:
			temporary_list.append(element)
			
			for index in range(1, row_or_column):
				temporary_list.append([x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])
			
			indices = []
			
			for index in temporary_list:
				indices.append(self.get_tile(index[0], index[1]))

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
		for row in range(self.grid_height):
			for col in range(self.grid_width):
				if self.get_tile(row, col) == 0:
					available_positions.append([row, col])
 
		if not available_positions:
			print "There are no available positions."
		else:
			random_tile = random.choice(available_positions)
 
			weighted_choices = [(1, 9), (2, 1)]
			population = [val for val, cnt in weighted_choices for i in range(cnt)]
			tile = random.choice(population)

			self.set_tile(random_tile[0],random_tile[1], tile)

	def get_available_moves(self):
		return filter(self.valid_move,[1,2,3,4])

	def get_available_rand_moves(self):
		available_positions = []
		for row in range(self.grid_height):
			for col in range(self.grid_width):
				if self.get_tile(row, col) == 0:
					available_positions.append([row, col,2])
					available_positions.append([row, col,4])
		return available_positions

	def set_tile(self, row, col, value):
		# Set the tile at position row, col to have the given value.
		x = 15 << 4*((self.grid_width*self.grid_height) - ((self.grid_width)*row + col) - 1)
		self.cells = self.cells | x

		y = 0xffffffffffffffff
		value1 = 15 - value
		y = y - (value1 << 4*((self.grid_width*self.grid_height) - ((self.grid_width)*row + col) - 1))
		self.cells = self.cells & y
				
	def get_tile(self, row, col):
		# Return the value of the tile at position row, col.
		x = 15 << 4*((self.grid_width*self.grid_height) - ((self.grid_width)*row + col) - 1)
		x = self.cells & x
		x = x >> 4*((self.grid_width*self.grid_height) - ((self.grid_width)*row + col) - 1)
		return x

	def next_state(self,direction):
		tmp = TwentyFortyEight(4, 4)
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.move(direction)
		return tmp

	def next_state_random(self,l):
		tmp = TwentyFortyEight(4, 4)
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.set_tile(l[0],l[1],l[2])
		return tmp

	def getColScore(self):
		x1 = TwentyFortyEight(4,4)
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				x1.set_tile(y, x, self.get_tile(x, y))
		return x1.getRowScore()

	def getRowScore(self):
		# print "In row score"
		# self.__str__()
		score = 0
		for x in range(self.grid_height):
			sum = 0
			prevTile = -1
			prevMerge = 0
			counter = 0
			empty = 0
			merges = 0
			mono_left = 0
			mono_right = 0

			for y in range(self.grid_width):
				val = self.get_tile(x, y)
				sum += self.get_tile(x, y)
				if(val == 0):
					empty += 1
				else:
					if(prevMerge == val):
						counter += 1
					elif(counter > 0):
						merges += 1 + counter
						counter = 0
					prevMerge = val
				if(prevTile >= 0):
					if(prevTile > val):
						# mono_left += prevTile
						mono_left += (prevTile ** SCORE_MONOTONICITY_POWER) - (val ** SCORE_MONOTONICITY_POWER)
					elif(prevTile < val):
						# mono_right += val
						mono_right += (val ** SCORE_MONOTONICITY_POWER) - (prevTile ** SCORE_MONOTONICITY_POWER)
				prevTile = val
			if(counter > 0):
				merges += 1+counter

			minMono = mono_left
			if(mono_left > mono_right):
				minMono = mono_right

			score += SCORE_LOST_PENALTY
			score += SCORE_EMPTY_WEIGHT * empty
			score += SCORE_MERGES_WEIGHT * merges
			score -= SCORE_MONOTONICITY_WEIGHT * minMono
			score -= SCORE_SUM_WEIGHT * sum

			# score += empty + merges - minMono - sum
			# print empty, merges, minMono, sum
			# print score

		# print "Out row score"
		return score

	def getBoardScore(self):
		# print self.getColScore()
		return self.getRowScore() + self.getColScore()

	def evaluate(self):
		# return self.maxValue()*self.score
		return self.getBoardScore()

	def isfilled(self):
		for x in range(self.grid_height):
			for y in range(self.grid_width):
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