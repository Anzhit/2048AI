from TwentyFortyEight import TwentyFortyEight
from AI import *

for i in range(100):
	x=TwentyFortyEight()
	x.make_tables()
	# x.print_tables()
	print("Generated Tables")
	x.new_tile()
	while(x.canMove()):
		x.__str__()
		dir=eminimax(x,3)
		# dir=minimax_alpha_beta(x,4)
		print(dir)
		print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
		x.move(dir)
		x.new_tile()
	print("GAME ENDs")
	print(x.maxValue())
	print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
	# x.__str__()
	# print(x.get_available_moves())