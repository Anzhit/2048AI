from TwentyFortyEight import TwentyFortyEight
import numpy as np
import random
import tensorflow as tf
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
	# #Random Sampling
	# if(len(avail_moves)>10):
	# 	weights=[ i[3] for i in avail_moves]
	# 	weights=np.array(weights)
	# 	weights /= weights.sum()
	# 	tmp=np.random.choice(len(avail_moves),10,replace=False,p=weights)
	# 	avail_moves=[avail_moves[i] for i in tmp]
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
	ans=0.0
	numRuns = 10

	if(game_state.maxValue() >= 16):
		numRuns = 20
	elif(game_state.maxValue() >= 32):
		numRuns = 50
	elif(game_state.maxValue() >= 256):
		numRuns = 75
	elif(game_state.maxValue() >= 512):
		numRuns = 120

	for i in range(numRuns):
		# print(i)
		tmp=TwentyFortyEight()
		tmp.cells=game_state.cells
		tmp.score=game_state.score


		count = 0
		while(tmp.canMove()):
			# count += 1
			# print(count)
			dir=random.choice([1,2,3,4])
			tmp.move(dir)
			tmp.new_tile()
			#print(game_state.cells)
		ans+=tmp.score1()
	ans /= numRuns

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

def expert_trained(game_state):
	#Fized sizes
	train_size = 556097
	input_size = 256
	Nlabels = 4
	out_size = 4
	test_size = 1829
	batch_size = 100
	init_var = 1e-2

	#Parameters
	learning_rate = 0.001
	training_epochs = 100
	hidden_1_size = 256
	hidden_2_size = 256

	sess = tf.InteractiveSession()


	W1 = tf.Variable(tf.random_normal([input_size, hidden_1_size], 0, init_var), name="W1")
	W2 = tf.Variable(tf.random_normal([hidden_1_size, hidden_2_size], 0, init_var), name="W2")
	Wout = tf.Variable(tf.random_normal([hidden_2_size, out_size], 0, init_var), name="Wout")


	b1 = tf.Variable(tf.random_normal([hidden_1_size], 0, init_var), name="b1")
	b2 = tf.Variable(tf.random_normal([hidden_2_size], 0, init_var), name="b2")
	bout = tf.Variable(tf.random_normal([out_size], 0, init_var), name="bout")

	def model(W1, b1, W2, b2, Wout, bout):
		# h = []
		# z = []
		# for i in range(n_layers):
		# 	h.append(tf.add(tf.matmul(x, W[i]), b[i]))
		# 	z.append(tf.nn.relu6(h[i]))
		# x_h1 = tf.nn.dropout(x, pkeep1)
		h1 = tf.add(tf.matmul(x1, W1), b1)
		z1 = tf.nn.relu6(h1)
		# z1_h2 = tf.nn.dropout(z1, pkeep1)
		h2 = tf.add(tf.matmul(z1, W2), b2)
		z2 = tf.nn.relu6(h2)

		# z2_out = tf.nn.dropout(z2, pkeep1)
		return tf.nn.softmax(tf.matmul(z2,Wout) + bout)

	x1 = tf.placeholder(tf.float32, shape=[None, input_size])
	y = model(W1, b1, W2, b2, Wout, bout)
	saver = tf.train.Saver()

	saver.restore(sess, "./model2.ckpt")

	temp = game_state.vectorize_state();
	tempx = np.zeros((1, 256))
	for j in range(16):
		tempx[0, j*16 + temp[j]] = 1

	probs=y.eval(feed_dict={x1: tempx})[0]
	# print(probs)
	# dir = eminimax(x,2)
	# dir=minimax_alpha_beta(x,6)
	# dir=monte_carlo(x)
	avail_moves = game_state.get_available_moves()
	if(len(avail_moves)==0):
		break
	# print(avail_moves)
	bestmove = avail_moves[0]-1
	for j in avail_moves:
		# print(j)
		if(probs[j-1]>probs[bestmove]):
			bestmove = j-1

	dir = bestmove+1