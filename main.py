from TwentyFortyEight import TwentyFortyEight
from AI import *

x=TwentyFortyEight()
x.new_tile()
while(x.canMove()):
	x.__str__()
	print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
	dir=eminimax(x,2)
	print(dir)
	x.move(dir)
	x.new_tile()