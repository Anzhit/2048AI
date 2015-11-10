from TwentyFortyEight import TwentyFortyEight

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
def eminimax(game_state,depth):

  return max(
	map(lambda move: (move, emin_play(game_state.next_state(move),depth,1.0)), 
	  game_state.get_available_moves()), 
	key = lambda x: x[1])[0]

def emin_play(game_state,depth,prob):
	if game_state.isfilled() or depth==0 or prob<0.005:
		return game_state.evaluate()
	avail_moves=game_state.get_available_rand_moves()
	prob /= len(avail_moves)
	return sum(
	map(lambda move: move[3]*emax_play(game_state.next_state_random(move),depth-1,prob*move[3]),
	  avail_moves))

def emax_play(game_state,depth,prob):
	if not(game_state.canMove()) or depth==0 or prob<0.005:
		return game_state.evaluate()
	return max(
	map(lambda move: emin_play(game_state.next_state(move),depth-1,prob),
	  game_state.get_available_moves()))


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