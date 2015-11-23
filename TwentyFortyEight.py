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
initial={
			UP : [[0,element] for element in range(4)],
			DOWN : [[4 - 1, element] for element in range(4)],
			LEFT : [[element, 0] for element in range(4)],
			RIGHT : [[element, 4 - 1] for element in range (4)]
		}
grid_height=4
grid_width=4
tableLeft = []
tableRight = []
heur_row_score ={}
class TwentyFortyEight:
	# Class to run the game logic.

	def __init__(self):
		# Initialize class
		self.cells = 0;
		self.score=0
		# self.print_tables()
		
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
		global grid_width
		global grid_height
		for i in range(grid_height):
			for j in range(1,grid_width):
				if self.get_tile(i,j-1)==self.get_tile(i,j) or self.get_tile(j-1,i)==self.get_tile(j,i):
					return True
				if self.get_tile(i,j-1)==0 or self.get_tile(i,j)==0 or self.get_tile(j-1,i)==0 or self.get_tile(j,i)==0:
					return True
		return False

	def move(self, direction):
		# Move all tiles in the given direction and add
		# a new tile if any tiles moved.
		global initial
		initial_list = initial[direction]

		# if(direction == UP):
		# 	self.move_helper(initial_list, direction, self.get_grid_height())
		# elif(direction == DOWN):
		# 	self.move_helper(initial_list, direction, self.get_grid_height())
		# elif(direction == LEFT):
		# 	self.move_helper(initial_list, direction, self.get_grid_width())
		# elif(direction == RIGHT):
		# 	self.move_helper(initial_list, direction,  self.get_grid_width())

		# print("Before", direction)
		# print(bin(self.cells))
		# self.__str__()
		# for row_or_column in range(grid_height):
		# 	print(bin(self.get_row(row_or_column)))

		self.move_helper_table(direction)
		# print("After")
		# self.__str__()

	def valid_move(self,direction):
		tmp = TwentyFortyEight()
		tmp.cells = self.cells
		tmp.move(direction)
		if(tmp.cells==self.cells):
			return False
		return True

	def move_helper_table(self, direction):
		# self.__str__()
		# print(direction)

		global tableLeft
		global tableRight
		global grid_height
		global grid_width
		if(direction == LEFT):
			for row_or_column in range(grid_height):
				self.set_row(row_or_column, tableLeft[self.get_row(row_or_column)])
		elif(direction == RIGHT):
			for row_or_column in range(grid_height):
				self.set_row(row_or_column, tableRight[self.get_row(row_or_column)])
		elif(direction == UP):
			for row_or_column in range(grid_width):
				self.set_colAsRow(row_or_column, tableLeft[self.get_colAsRow(row_or_column)])
				# print("Step #", row_or_column)
				# self.__str__()
		elif(direction == DOWN):
			for row_or_column in range(grid_width):
				# print(bin(self.get_colAsRow(row_or_column)))
				# print(bin(tableRight[self.get_colAsRow(row_or_column)]))
				self.set_colAsRow(row_or_column, tableRight[self.get_colAsRow(row_or_column)])


	def print_tables(self):
		global tableLeft
		global tableRight
		print("Left Table")
		for i in range(65536):
			nums = []
			for j in range(grid_height):
				x = i >> 4*j
				x = x & 15
				nums.append(x)
			print(bin(i), end=" ")
			print(" -- ", end=" ")
			print(bin(tableLeft[i]))
		
		print("Right Table\n")
		for i in range(65536):
			nums = []
			for j in range(grid_height):
				x = i >> 4*j
				x = x & 15
				nums.append(x)
			print(nums, end=" ")
			print(" -- ", end=" ")
			print(tableRight[i])

	def make_tables(self):
		global tableRight
		global tableLeft
		global grid_height
		tableLeft = []
		tableRight = []
		for row in range(65536):
			vals = []
			for i in range(grid_height):
				x = row >> 4*(grid_height - i - 1)
				x = x & 15
				vals.append(x)
			# print(vals, end = " ")
			val = list(vals)
			leftVals = self.mergeLeft(val)
			val = list(vals)
			rightVals = self.mergeRight(val)
			# print(leftVals, rightVals)

			leftNum = 0
			for i in leftVals:
				leftNum = (leftNum << 4) + i
			rightNum = 0
			for i in rightVals:
				rightNum = (rightNum << 4) + i

			tableLeft.append(leftNum)
			tableRight.append(rightNum)

		# print(len(valsLeft), len(valsRight))

	def mergeLeft(self, nums):
		size = len(nums)
	  # remove all the zeroes
		nums[:] = (value for value in nums if value != 0)
	  # now do the merging, use an index to run through the list
		i = 0
		while (i < len(nums)-1 ):
			if (nums[i]==nums[i+1]): # if a number is the same as the following
				nums[i] += 1           # double it 
				del nums[i+1]          # remove the following
				# self.score+=1<<nums[i]         # Increment Score
			i += 1
	  # restore the initial list length appending zeroes
		while (len(nums) < size):
			nums.append(0)
	  # done
		return nums

	def mergeRight(self, nums):
		size = len(nums)
	  # remove all the zeroes
		nums[:] = (value for value in nums if value != 0)
	  # now do the merging, use an index to run through the list
		i = len(nums) - 1
		while (i > 0):
			if (nums[i]==nums[i-1]): # if a number is the same as the following
				nums[i] += 1           # double it 
				del nums[i-1]          # remove the following
				i -= 1
				# self.score+=1<<nums[i]         # Increment Score
			i -= 1
	  # restore the initial list length appending zeroes
		while (len(nums) < size):
			nums = [0] + nums
	  # done
		return nums

	def move_helper(self, initial_list, direction, row_or_column):
		# Move all columns and merge
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
			return
		else:
			random_tile = random.choice(available_positions)
			x=random.randint(0,9)
			if x==0:
				tile=2
			else:
				tile=1
			self.set_tile(random_tile[0],random_tile[1], tile)

	def get_available_moves(self):
		ans=[]
		for i in [1,2,3,4]:
			tmp = TwentyFortyEight()
			tmp.cells = self.cells
			tmp.move(i)
			if(not(tmp.cells==self.cells)):
				ans.append([i,tmp])
		return ans

	def get_available_rand_moves(self):
		global grid_width
		global grid_height
		available_positions = []
		for row in range(grid_height):
			for col in range(grid_width):
				if self.get_tile(row, col) == 0:
					available_positions.append((row, col,1,0.9))
					available_positions.append((row, col,2,0.1))
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
				
	def get_row(self, row):
		# Return the row at position row.
		global grid_width
		global grid_height
		r = 65535 << 4*((grid_width * (grid_height - row - 1)))
		r = self.cells & r
		r = r >> 4*((grid_width * (grid_height - row - 1)))
		return r

	def set_row(self, row, value):
		# Set the tile at position row, col to have the given value.
		global grid_width
		global grid_height
		x = 65535 << 4*((grid_width * (grid_height - row - 1)))
		self.cells = self.cells | x

		y = 0xffffffffffffffff
		value1 = 65535 - value
		y = y - (value1 << 4*((grid_width * (grid_height - row - 1))))
		self.cells = self.cells & y

	def get_colAsRow(self, col):
		global grid_width
		global grid_height
		r = 0
		for row in range(grid_height):
			x = 15 << (4*((grid_width*grid_height) - ((grid_width)*row + col) - 1))
			x = self.cells & x
			r = (r << 4) + (x >> 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1))
		return r

	def set_colAsRow(self, col, value):
		# print("Before setting column #", col, " to ", value)
		# self.__str__()
		# Set the tile at position row, col to have the given value.
		global grid_width
		global grid_height
		for rowIterator in range(grid_height):
			row = grid_height - rowIterator - 1
			x = 15 << (4*((grid_width*grid_height) - ((grid_width)*row + col) - 1))
			self.cells = self.cells | x

			y = 0xffffffffffffffff

			valueTemp = value & 15
			value1 = 15 - valueTemp
			y = y - (value1 << 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1))
			self.cells = self.cells & y
			value = value >> 4

		# print("After setting column #", col, " to ", value)
		# self.__str__()

	def get_tile(self, row, col):
		# Return the value of the tile at position row, col.
		global grid_width
		global grid_height
		x = 15 << 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1)
		x = self.cells & x
		x = x >> 4*((grid_width*grid_height) - ((grid_width)*row + col) - 1)
		return x

	def next_state_random(self,l):
		tmp = TwentyFortyEight()																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																										
		tmp.score = self.score
		tmp.cells = self.cells
		tmp.set_tile(l[0],l[1],l[2])
		return tmp

	def getColScore(self):
		global grid_width
		global grid_height
		x1 = TwentyFortyEight()
		for x in range(grid_width):
			for y in range(grid_height):
				x1.set_tile(y, x, self.get_tile(x, y))
		return x1.getRowScore()
	def get_row(self, row):
		# Return the row at position row.
		global grid_width
		global grid_height
		r = 0xffff << 4*((grid_width * (grid_height - row - 1)))
		r = self.cells & r
		r = r >> 4*((grid_width * (grid_height - row- 1)))
		return r
	def getRowScore(self):
		# print "In row score"
		# self.__str__()
		global grid_width
		global grid_height
		score = 0
		for x in range(grid_height):
			sum = 0
			prevTile = -1
			prevMerge = 0
			counter = 0
			empty = 0
			merges = 0
			mono_left = 0
			mono_right = 0
			row=self.get_row(x)
			if(row in heur_row_score):
				score+= heur_row_score[row]
			else:
				tscore=0
				for y in range(grid_width):
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
						else:
							# mono_right += val
							mono_right += (val ** SCORE_MONOTONICITY_POWER) - (prevTile ** SCORE_MONOTONICITY_POWER)
					prevTile = val
				if(counter > 0):
					merges += 1+counter

				minMono = mono_left
				if(mono_left > mono_right):
					minMono = mono_right

				tscore += SCORE_LOST_PENALTY
				tscore += SCORE_EMPTY_WEIGHT * empty
				tscore += SCORE_MERGES_WEIGHT * merges
				tscore -= SCORE_MONOTONICITY_WEIGHT * minMono
				tscore -= SCORE_SUM_WEIGHT * sum
				score+=tscore
				heur_row_score[row]=tscore
			# score += empty + merges - minMono - sum
			# print empty, merges, minMono, sum
			# print score

		# print "Out row score"
		return score
		
	def evaluate(self):
		# return self.maxValue()*self.score
		return self.getRowScore() + self.getColScore()

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