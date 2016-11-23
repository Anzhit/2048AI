from __future__ import print_function
from TwentyFortyEight import TwentyFortyEight
from AI import *
import tensorflow as tf
import numpy as np
import math

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

# action = tf.argmax(y,1)

# for i in range(1):
# 	x=TwentyFortyEight()
# 	x.make_tables()
# 	# x.print_tables()
# 	print("Generated Tables")
# 	x.new_tile()
# 	while(x.canMove()):
# 		x.__str__()
# 		# dir=eminimax(x,4)
# 		dir=minimax_alpha_beta(x,7)
# 		print(dir)
# 		print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
# 		x.move(dir)
# 		x.new_tile()
# 	# print("GAME ENDs")
# 	# print(x.maxValue())
# 	print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
# 	# x.__str__()
# 	# print(x.get_available_moves())



occ = np.zeros(16)
for i in range(500):
	x=TwentyFortyEight()
	x.make_tables()
	# x.print_tables()
	# print("Generated Tables")
	x.new_tile()
	# avail_moves = x.get_available_moves()
	while(True):
		# x.__str__()
		# print("-----------------------")
		temp = x.vectorize_state();
		tempx = np.zeros((1, 256))
		for j in range(16):
			tempx[0, j*16 + temp[j]] = 1

		probs=y.eval(feed_dict={x1: tempx})[0]
		# print(probs)
		# dir = eminimax(x,2)
		# dir=minimax_alpha_beta(x,6)
		# dir=monte_carlo(x)
		avail_moves = x.get_available_moves()
		if(len(avail_moves)==0):
			break
		# print(avail_moves)
		bestmove = avail_moves[0]-1
		for j in avail_moves:
			# print(j)
			if(probs[j-1]>probs[bestmove]):
				bestmove = j-1

		dir = bestmove+1
		# print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
		x.move(dir)
		x.new_tile()
	# print("GAME ENDs")
	# print(x.maxValue())
	print("Score:"+str(x.score)+"\t Max Tile:"+str(x.maxValue()))
	occ[int(math.log(x.maxValue(), 2))] += 1
	# print(occ)
	# x.__str__()
	# print(x.get_available_moves())

for i in range(16):
	print(1<<i, " : ", occ[i])