from TwentyFortyEight import TwentyFortyEight
from AI import *

for c in range(10):
	x=TwentyFortyEight()
	x.new_tile()
	# x.__str__()
	# print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
	dir=minimax_alpha_beta(x,6)
	# print(dir)
	# x.move(dir)