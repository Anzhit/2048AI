import tensorflow as tf
import numpy as np
from TwentyFortyEight import TwentyFortyEight
import random
import matplotlib.pyplot as plt
from AI import eminimax

SUMMARY_DIR = './results'

class Environment(object):

    def __init__(self):
        self.S=TwentyFortyEight()
        self.S.make_tables()
        self.score=0
        self.S.new_tile()
        print("New Episode")
    def reset(self):
        self.S.score=0
        self.S.cells=0
        self.score=0
        self.S.new_tile()
        return self.S.vectorize_state()
    def step(self,action):
        score_prev = self.S.score1()
        cells=self.S.cells
        self.S.move(action+1)
        r=self.S.score1()-score_prev
        self.score=self.S.score1()
        if(not cells==self.S.cells):
            self.S.new_tile()
        if(not self.S.canMove()):
            return self.S.vectorize_state(),r,True
        return self.S.vectorize_state(),r,False
    def seed(self,a):
        return

env = Environment()

inputs1 = tf.placeholder(shape=[1,16],dtype=tf.float32)
W = tf.Variable(tf.random_normal([16,200],0, 0.01))
W1 = tf.Variable(tf.random_normal([200,100],0,0.01))
W2 = tf.Variable(tf.random_normal([100,50],0,0.01))
W3 = tf.Variable(tf.random_normal([50,4],0,0.01))

Qout = tf.matmul(tf.nn.relu(tf.matmul(tf.nn.relu(tf.matmul(tf.nn.relu(tf.matmul(inputs1,W)),W1)),W2)),W3)
predict = tf.argmax(Qout,1)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.AdamOptimizer(learning_rate=0.001)
updateModel = trainer.minimize(loss)
init = tf.initialize_all_variables()

# Set learning parameters
y = 0.1
e = 0.1
num_episodes = 1000
#create lists to contain total rewards and steps per episode
jList = []
rList = []
QmaxList = []
with tf.Session() as sess:
    sess.run(init)
    writer = tf.train.SummaryWriter(SUMMARY_DIR, sess.graph)

    # summary1 = tf.Variable(0.)
    # summary2 = tf.Variable(0.)

    # tf.scalar_summary("Sum", summary1)
    # tf.scalar_summary("Qmax Value", summary2)
    # summary_vars = [summary1, summary2]
    # summary_ops = tf.merge_all_summaries()


    for i in range(num_episodes):
        #Reset environment and get first new observation
        s = env.reset()
        rAll = 0
        d = False
        j = 0
        avgQmax = 0
        #The Q-Network
        while True:
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
            # print("maxQ1",maxQ1)
            # print("r:", r)
            avgQmax += maxQ1
            targetQ = allQ
            targetQ[0,a[0]] = r + y*maxQ1
            #Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:[s],nextQ:targetQ})
            rAll += r
            s = s1
            # print("action:", a[0])
            if d == True:
                #Reduce chance of random action as we train the model.
                e = 1./((i/20) + 5)
                break

        print("j:", j)
        avgQmax = float(avgQmax) / float(j)
        jList.append(rAll)
        print("Ep no:", i)
        print("Sum tiles:", jList[len(jList)-1])
        max_value = env.S.maxValue()
        print("Max value:", max_value)
        print("Avg Qmax :", avgQmax)
        QmaxList.append(avgQmax)
        # summary1_op = tf.assign(jList[len(jList)-1])
        # summary2_op = tf.assign(max_value)

        # sess.run(summary1_op);
        # sess.run(summary2_op);
        # sess.run(summary_ops, feed_dict={
        #             summary_vars[0]: jList[len(jList)-1],
        #             summary_vars[1]: max_value
        #         })
# plt.plot(QmaxList)
# plt.show()
plt.plot(jList)
plt.show()