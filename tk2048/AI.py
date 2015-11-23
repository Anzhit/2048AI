from TwentyFortyEight import TwentyFortyEight
import numpy as np
import random
table ={}
table1={}
def minimax_alpha_beta(game_state,depth):

  return max(
	map(lambda move: (move, ABmin_play(move[1],-float('inf'),float('inf'),depth)), 
	  game_state.get_available_moves()), 
	key = lambda x: x[1])[0][0]

def ABmin_play(game_state,alpha,beta,depth):
	if game_state.isfilled() or depth==0:
		score=game_state.evaluate()
		return score
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
		v = max(v, ABmin_play(move[1], alpha, beta, depth-1))
		if v >= beta:
			return v
		alpha = max(alpha, v)
	return v
def eminimax(game_state,depth):

  return max(
	map(lambda move: (move, emin_play(move[1],depth,1.0)), 
	  game_state.get_available_moves()), 
	key = lambda x: x[1])[0][0]

def emin_play(game_state,depth,prob):
	if game_state.cells in table:
		if table[game_state.cells][1]>=depth:
			return table[game_state.cells][0]
	if game_state.isfilled() or depth==0 or prob<0.0001:
		return game_state.evaluate()
	avail_moves=game_state.get_available_rand_moves()
	prob /= len(avail_moves)
	#Random Sampling
	if(len(avail_moves)>10):
		weights=[ i[3] for i in avail_moves]
		weights=np.array(weights)
		weights /= weights.sum()
		tmp=np.random.choice(len(avail_moves),10,replace=False,p=weights)
		avail_moves=[avail_moves[i] for i in tmp]
	x = sum(
	map(lambda move: (move[3]/len(avail_moves))*emax_play(game_state.next_state_random(move),depth-1,prob*move[3]),
	  avail_moves))
	table[game_state.cells]=(x,depth)
	return x

def emax_play(game_state,depth,prob):
	if game_state.cells in table1:
		if table1[game_state.cells][1]>=depth:
			return table1[game_state.cells][0]
	if not(game_state.canMove()) or depth==0:
		return game_state.evaluate()
	x= max(
	map(lambda x: emin_play(x[1],depth-1,prob),
	  game_state.get_available_moves()))
	table1[game_state.cells]=(x,depth)
	return x

def monte_carlo(game_state):
  return max(
	map(lambda move: (move, monte_play(move[1])), 
	  game_state.get_available_moves()), 
	key = lambda x: x[1])[0][0]
def monte_play(game_state):
	ans=0
	for i in range(100):
		while(game_state.canMove()):
			dir=random.choice(game_state.get_available_moves())
			game_state.cells=dir[1].cells
			game_state.new_tile()
			#print(game_state.cells)
		ans+=game_state.score

	return ans

def minimax(game_state,depth):

  return max(
	map(lambda move: (move, min_play(move[1],depth)), 
	  game_state.get_available_moves()), 
	key = lambda x: x[1])[0][0]

def min_play(game_state,depth):
	if game_state.isfilled() or depth==0:
		score=game_state.evaluate()
		return score
	return min(
	map(lambda move: max_play(game_state.next_state_random(move),depth-1),
		game_state.get_available_rand_moves()))

def max_play(game_state,depth):
	if not(game_state.canMove()) or depth==0:
		return game_state.evaluate()
	return max(
	map(lambda move: min_play(move[1],depth-1),
	  game_state.get_available_moves()))