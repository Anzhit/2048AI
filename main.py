from TwentyFortyEight import TwentyFortyEight
from AI import *

x=TwentyFortyEight()
x.new_tile()
while(x.canMove()):
	x.__str__()
	print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
	dir=minimax_alpha_beta(x,4)
	print(dir)
	x.move(dir)