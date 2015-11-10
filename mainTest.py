from TwentyFortyEight import TwentyFortyEight
from AI import *

x=TwentyFortyEight(4,4)
x.new_tile()
for c in range(50):
	# x.__str__()
	# print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
	dir=minimax_alpha_beta(x,8)
	# print(dir)
	x.move(dir)