import common as cm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

testPerc = 0.5
data = cm.readNumpy("datasets/data.csv",'label')
[X,y,headers] = data
X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=testPerc, random_state=43)

def plot2D(X,y):
	#plt.title('')
	#plt.xlabel('n') 
	#plt.ylabel('y (0\'s) ') 
	#axes = plt.gca()
	#axes.set_xlim([-100,1200])
	#axes.set_ylim([-100,350])
	plt.scatter(X[:,0], X[:,1],  c=y, s=100)
	#plt.scatter(X_train, y_train,  color='black', s=30)
	#plt.plot(X[:,0], regr.predict(X), color='blue', linewidth=3, alpha=0.4)
	#plt.plot(X, y, color='green', linewidth=3, alpha=0.4)
	plt.show()

def plot3D(X,y):
	print y
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	plt.title('Red = 1, Blue = 0')
	ax.scatter(X[:,1], X[:,2], X[:,0], c=y, s=200)
	ax.set_xlabel('x')
	ax.set_ylabel('p1')
	ax.set_zlabel('y')
	plt.show()

#def replace(y,):
#	n  = y[:]


#plot3D(X,y)
plot2D(X,y)