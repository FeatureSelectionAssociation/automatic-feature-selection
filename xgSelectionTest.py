# plot feature importance using built-in function
from numpy import argsort
from xgboost import XGBClassifier
import classifiers as cf
from pandas import read_csv, np
import time
import cuts

def  xgRelevancy(X,y):
	model = XGBClassifier()
	model.fit(X, y)
	featureImportance = model.feature_importances_
	indexorder = argsort(featureImportance)
	indexorder = list(indexorder)
	indexorder.reverse()
	return [featureImportance, indexorder]

def xgTest():
	#Artifial Datasets
	files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv','data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv','data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv','data1000-f1-r500.csv','data5000-f1-r500.csv','data20000-f1-r500.csv']
	buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,2,3,4,5,6,13,14],[0,1,2,3,4,5,6,13,14]]	
	#Real Datasets
	#files = ['real/sonar_scale.csv', 'real/splice_scale.csv', 'real/colon-cancer.csv', 'real/leu.csv', 'real/duke.csv', 'real/BH20000.csv', 'real/madelon-test.csv']
	#buenos = [['?'],['?'],['?'],['?'],['?'],['?'],['?']]
	i=0
	verboseClassifiers = True
	for f in files:
		filepath = 'Data/'+f		
		data = read_csv(filepath)
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		print filepath, buenos[i]
		startTime = time.time()
		acc = cf.getBestClassifiers(X,y)
		endTime = time.time()
		print "original:", acc, X.shape[1], str(round(endTime-startTime,3))+"s"
		try:
			startTime = time.time()
			[featureImportance, rank] = xgRelevancy(X,y)
			cutpos = cuts.monotonicValidationCut(X,y,rank)
			rank = rank[0:cutpos]
			endTime = time.time()
			timefs = round(endTime-startTime,3)
			X = np.array(data.ix[:,rank])
			startTime = time.time()
			acc = cf.getBestClassifiers(X,y)
			endTime = time.time()
			timecf = round(endTime-startTime,3)
			print "result: ",acc, timefs, timecf, len(rank), rank[0:5]
			print 	
		except Exception as inst:
			X = np.array(data.ix[:,0:-1])
			print "error"

if __name__ == '__main__':
	xgTest()

