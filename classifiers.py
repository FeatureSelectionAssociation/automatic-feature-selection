from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

names = [
		"NearestNeighbors",
		"DecisionTree",
		"RandomForest",
		"AdaBoost"
		]

classifiers = [
		KNeighborsClassifier(10),
		DecisionTreeClassifier(max_depth=5),
		RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
		AdaBoostClassifier()
    ]

def getBestClassifiers(X,y,testPerc=0.4):
	global classifiers
	global names
	X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=testPerc, random_state=43)
	fscore = 0
	for name, clf in zip(names, classifiers):
		clf.fit(X_train, y_train)
		score = clf.score(X_test, y_test)
		fscore += score
	return round(fscore/len(classifiers),2)