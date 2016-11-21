import tensorflow as tf
import numpy as np
from TwentyFortyEight import TwentyFortyEight
import random
import matplotlib.pyplot as plt
class Environment(object):

    def __init__(self):
        self.S=TwentyFortyEight()
        self.S.make_tables()
        self.score=0
        self.S.new_tile()
        print("New Episode")
    def reset(self):
        self.S=TwentyFortyEight()
        self.S.make_tables()
        self.score=0
        self.S.new_tile()
        return self.S.vectorize_state()
    def step(self,action):
        self.S.move(action+1)
        r=self.S.score1()-self.score
        self.score=self.S.score1()
        self.S.new_tile()
        if(not self.S.canMove()):
            return self.S.vectorize_state(),r,True
        return self.S.vectorize_state(),r,False
    def seed(self,a):
        return

env = Environment()

inputs1 = tf.placeholder(shape=[1,17],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([17,100],0,0.01))
W1 = tf.Variable(tf.random_uniform([100,4],0,0.01))
Qout = tf.matmul(tf.nn.relu(tf.matmul(inputs1,W)),W1)
predict = tf.argmax(Qout,1)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.AdamOptimizer(learning_rate=0.001)
updateModel = trainer.minimize(loss)
init = tf.initialize_all_variables()

# Set learning parameters
y = 1
e = 0.1
num_episodes = 10000
#create lists to contain total rewards and steps per episode
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        #Reset environment and get first new observation
        s = env.reset()
        rAll = 0
        d = False
        j = 0
        #The Q-Network
        while j < 1000:
            j+=1
            #Choose an action by greedily (with e chance of random action) from the Q-network
            a,allQ = sess.run([predict,Qout],feed_dict={inputs1:[s]})
            if np.random.rand(1) < e:
                a[0] = random.randint(0,3)
            #Get new state and reward from environment
            s1,r,d = env.step(a[0])
            #Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout,feed_dict={inputs1:[s1]})
            #Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0,a[0]] = r + y*maxQ1
            #Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:[s],nextQ:targetQ})
            rAll += r
            s = s1
            if d == True:
                #Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                break
        jList.append(rAll)
        print(jList)
plt.plot(jList)
plt.show()