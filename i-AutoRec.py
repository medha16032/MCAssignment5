
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:26:21 2017

@author: Medha Gupta
"""


import tensorflow as tf
import numpy as np
import math


train='u2_train.txt'
test='u2_test.txt'
# Training Parameters
learning_rate = 0.01
num_steps = 3000
batch_size = 1682

display_step = 100

lambda_val=0.01

noOfMovies=1682
noOfUsers=943

ratingMatrix=np.zeros((noOfMovies, noOfUsers))
binaryMatrix=np.zeros((noOfMovies, noOfUsers))


with open (train) as fp:
    for line in fp:        
        userId=line.split("\t")[0]
        movieId=line.split("\t")[1]
        rating=line.split("\t")[2]
        userIdInt=int(userId)
        movieIdInt=int(movieId)
        ratingInt=int(rating)
        ratingMatrix[movieIdInt-1][userIdInt-1]=ratingInt
        binaryMatrix[movieIdInt-1][userIdInt-1]=1

# Network Parameters
num_hidden_1 = 100 # 1st layer num features
#num_hidden_2 = 128 # 2nd layer num features (the latent dim)
num_input = 943 # MNIST data input (img shape: 28*28)

# tf Graph input (only pictures)
X = tf.placeholder("float", [None, num_input])
Y=  tf.placeholder("float", [None, num_input])

weights = {
    'encoder_h1': tf.Variable(tf.random_normal([num_input, num_hidden_1])),
    'decoder_h1': tf.Variable(tf.random_normal([num_hidden_1, num_input])),
}
biases = {
    'encoder_b1': tf.Variable(tf.random_normal([num_hidden_1])),
    'decoder_b1': tf.Variable(tf.random_normal([num_input])),   
}

# Building the encoder
def encoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   biases['encoder_b1']))    
    return layer_1


# Building the decoder
def decoder(x):
    # Decoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']),
                                   biases['decoder_b1']))
    
    return layer_1

# Construct model
encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

# Prediction
y_pred = decoder_op
# Targets (Labels) are the input data.
y_true = X

# Define loss and optimizer, minimize the squared error
loss = tf.reduce_mean(tf.pow(y_true - y_pred*Y, 2))+(lambda_val/2)*(tf.norm(weights['encoder_h1']) + tf.norm(weights['decoder_h1']))
optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(loss)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()



sess=tf.Session()
sess.run(init)

scaledRatingMatrix=np.divide(ratingMatrix-np.min(ratingMatrix),5)


for i in range(1, num_steps+1):
    # Run optimization op (backprop) and cost op (to get loss value)
    _, l = sess.run([optimizer, loss], feed_dict={X: scaledRatingMatrix, Y:binaryMatrix})
    # Display logs per step
    if i % display_step == 0 or i == 1:
        print('Step %i: batch Loss: %f' % (i, l))

predictedRatings=sess.run(decoder_op, feed_dict={X: scaledRatingMatrix, Y:binaryMatrix})



count=0
MAESum=0.0
with open (test) as fp1:
    for line in fp1:
        count=count+1        
        userId=line.split("\t")[0]
        movieId=line.split("\t")[1]
        rating=line.split("\t")[2]
        userIdInt=int(userId)
            
        movieIdInt=int(movieId)
        ratingInt=int(rating)
            
        prating=predictedRatings[movieIdInt-1][userIdInt-1]*5        
        error=math.fabs(prating-ratingInt)
        MAESum=error+MAESum
                
MAE=MAESum/(count)
#NMAE=NMAE/4.0
print(MAE)


