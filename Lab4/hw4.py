import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

#Be careful with the file path!
data = loadmat('data/hw4.mat') # type(data) = dict
#print(data['X'].size) = 5000 * 400 data['X'] type:numpy.ndarray
#print(data['y'].size) = 5000
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(sparse=False)
y_onehot = encoder.fit_transform(data['y'])

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def forward_propagate(X, theta1, theta2):
    m = X.shape[0]

    #Write codes here
    a1 = X
    theta1_tranpose = theta1.transpose()
    theta1_bias = theta1_tranpose[theta1_tranpose.shape[0] - 1]
    theta1_tranpose = np.delete(theta1_tranpose, theta1_tranpose.shape[0] - 1, axis=0)
    z2 = np.dot(X, theta1_tranpose)
    for i in range(0, X.shape[0]):
        z2[i] = z2[i] + theta1_bias
    activate = lambda i : sigmoid(i)
    vectorized_activate = np.vectorize(activate)
    a2 = vectorized_activate(z2)
    theta2_tranpose = theta2.transpose()
    theta2_bias = theta2_tranpose[theta2_tranpose.shape[0] - 1]
    theta2_tranpose = np.delete(theta2_tranpose, theta2_tranpose.shape[0] - 1, axis=0)
    z3 = np.dot(a2, theta2_tranpose)
    for i in range(0, a2.shape[0]):
        z3[i] = z3[i] + theta2_bias
    h = vectorized_activate(z3)
    
    return a1, z2, a2, z3, h

def cost(params, input_size, hidden_size, num_labels, X, y, learning_rate):
    m = X.shape[0] # 5000
    X = np.matrix(X)
    y = np.matrix(y)
    # reshape the parameter array into parameter matrices for each layer
    theta1 = np.matrix(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
    theta2 = np.matrix(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))
    # run the feed-forward pass
    a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)
    # compute the cost
    J = 0
    for i in range(m):
        first_term = np.multiply(-y[i,:], np.log(h[i,:]))
        second_term = np.multiply((1 - y[i,:]), np.log(1 - h[i,:]))
        J += np.sum(first_term - second_term)
        
    J = J / m
    J += (float(learning_rate) / (2*m) * (np.sum(np.power(theta1[:,1:], 2)) + np.sum(np.power(theta2[:,1:]))))
    
    return J
    
# initial setup
input_size = 400
hidden_size = 10
num_labels = 10
learning_rate = 1
# randomly initialize a parameter array of the size of the full network's parameters
params = (np.random.random(size=hidden_size * (input_size + 1) + num_labels * (hidden_size + 1)) - 0.5) * 0.2
m = data['X'].shape[0]
X = np.matrix(data['X'])
y = np.matrix(data['y'])
# unravel the parameter array into parameter matrices for each layer
theta1 = np.matrix(np.reshape(params[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1)))) #10*401
theta2 = np.matrix(np.reshape(params[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1)))) #10*11

a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)

def sigmoid_gradient(z):
    return np.multiply(sigmoid(z), (1 - sigmoid(z)))    
'''
def backprop(params, input_size, hidden_size, num_labels, X, y, learning_rate):
    m = X.shape[0]
   
    #Write codes here
    
    return J, grad
    
from scipy.optimize import minimize
# minimize the objective function
fmin = minimize(fun=backprop, x0=params, args=(input_size, hidden_size, num_labels, X, y_onehot, learning_rate), method='TNC', jac=True, options={'maxiter': 250})
      
X = np.matrix(X)
theta1 = np.matrix(np.reshape(fmin.x[:hidden_size * (input_size + 1)], (hidden_size, (input_size + 1))))
theta2 = np.matrix(np.reshape(fmin.x[hidden_size * (input_size + 1):], (num_labels, (hidden_size + 1))))
a1, z2, a2, z3, h = forward_propagate(X, theta1, theta2)
y_pred = np.array(np.argmax(h, axis=1) + 1)

correct = [1 if a == b else 0 for (a, b) in zip(y_pred, y)]
accuracy = (sum(map(int, correct)) / float(len(correct)))
print ('accuracy = {0}%'.format(accuracy * 100))
'''