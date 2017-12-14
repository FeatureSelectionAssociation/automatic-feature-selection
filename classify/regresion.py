import common as cm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

testPerc = 0.5
#data = cm.readNumpy("datasets/factorial15.csv",'label') 
data = cm.readNumpy("datasets/factorial.csv",'label') 
[X,y,headers] = data
X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=testPerc, random_state=43)
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
#'''
# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(X_test) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_test, y_test))
#'''
# Plot outputs
#'''
plt.title('Linear Regresion')
#plt.xlabel('n') 
#plt.ylabel('y (0\'s) ') 
#axes = plt.gca()
#axes.set_xlim([-100,1200])
#axes.set_ylim([-100,350])
plt.scatter(X_test[:,0], y_test,  color='red', marker='*', s=40)
plt.scatter(X_train[:,0], y_train,  color='black', s=30)
#plt.plot(X[:,0], regr.predict(X), color='blue', linewidth=3, alpha=0.4)
#plt.plot(X, y, color='green', linewidth=3, alpha=0.4)
plt.plot(X, regr.predict(X), color='blue', linewidth=3, alpha=0.4)
plt.show()
#'''

print np.around(regr.predict(X),decimals=0)
print np.around(regr.predict(3000))
print np.around(regr.predict(10001))
print np.around(regr.predict(100001))
print np.around(regr.predict(1000001))