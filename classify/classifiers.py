import common as cm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import Perceptron
#import xgboost as xgb


names = [
		#"Perceptron",
		#"XGBreglinear",
		#"XGBreglogistic",
		"NearestNeighbors",
		"LinearSVM", 
		"DecisionTree",
		"RandomForest",
		"AdaBoost",
		#"NeuralNet",
		"NaiveBayes", 
		#"LDA",
		#"QDA"
		]

classifiers = [
		#Perceptron(),
		#xgb.XGBClassifier(objective='reg:linear'),
		#xgb.XGBClassifier(objective='reg:logistic'),
		KNeighborsClassifier(10),
		SVC(kernel="linear"),
		DecisionTreeClassifier(max_depth=5),
		RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
		AdaBoostClassifier(),
		#MLPClassifier(verbose=False),
		GaussianNB(),
		#LinearDiscriminantAnalysis(),
		#QuadraticDiscriminantAnalysis()
    ]



def getBestClassifiers(names,classifiers, doTest=False, testPerc=0.5):
	#Train and validate
	data = cm.readNumpy("../Data/colon-cancer-fs2.csv",'label') #0.595l 0.6147 0.7086 "clean" dataset
	[X,y,headers] = data
	X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=testPerc, random_state=43)
	#print X_train
	
	#plt.title("data", fontsize='small')
	#plt.scatter(X_train[:, 0], X_train[:, 1], marker='o', c=y_train)
	#plt.show()

	for name, clf in zip(names, classifiers):
		clf.fit(X_train, y_train)
		score = clf.score(X_test, y_test)
		#print X_test
		#print y_test
		#print clf.predict(X_test)
		print (name, round(score,2))		

	
getBestClassifiers(names,classifiers, doTest=True, testPerc=0.25)
