import model as ml
import featureSelection as fs
from pandas import read_csv, np
import time
def artificialTest():
	#Artifial Datasets
	#files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv','data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv','data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv','data1000-f1-r500.csv','data5000-f1-r500.csv','data20000-f1-r500.csv']
	#Real Datasets
	#files = ['real/classification/1c.csv', 'real/classification/2c.csv', 'real/classification/3c.csv', 'real/classification/4c.csv', 'real/classification/5c.csv', 'real/classification/6c.csv', 'real/classification/7c.csv', 'real/classification/8c.csv', 'real/classification/9c.csv', 'real/classification/10c.csv', 'real/classification/11c.csv', 'real/classification/12c.csv', 'real/classification/13c.csv', 'real/classification/14c.csv', 'real/classification/15c.csv', 'real/classification/16c.csv', 'real/classification/17c.csv']
	files = ['real/classification/2r.csv']
	modelTypes = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	i=0
	verboseClassifiers = True
	for f in files:
		modelType = modelTypes[i]
		maxAcc = 0
		maxRank = []
		configuration = []	
		filepath = 'Data/'+f		
		data = read_csv(filepath)
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		print filepath
		startTime = time.time()
		acc = ml.modelJudge(X=X, y=y, modelType=modelType, testPerc=0.4, runs=3)
		endTime = time.time()
		print "original:", acc, X.shape[1], str(round(endTime-startTime,3))+"s"
		for minRed in [0,1]:#range(0,2):
			for binMethod in [0]:#range(0,2):
				for cutMethod in [1,3]:#range(0,4):
					for corrOption in [1,3]:#range(0,6):
						#try:
						startTime = time.time()
						rank = fs.featureSelection(X=X,y=y, modelType=modelType, runs=3, processes=0, corrOption=corrOption, binMethod=binMethod, cutMethod=cutMethod, minRed=minRed, debug=False)							
						endTime = time.time()
						timefs = round(endTime-startTime,3)
						X = np.array(data.ix[:,rank])
						startTime = time.time()
						acc = ml.modelJudge(X=X, y=y, modelType=modelType, testPerc=0.4, runs=3)
						endTime = time.time()
						timecf = round(endTime-startTime,3)
						print minRed,binMethod, cutMethod, corrOption, acc, timefs, timecf, len(rank), rank[0:5]			
						if(acc>maxAcc):
							maxAcc = acc
							maxRank = rank
							configuration = [minRed,binMethod,cutMethod,corrOption]
						X = np.array(data.ix[:,0:-1])
						#except Exception as inst:
						#	X = np.array(data.ix[:,0:-1])
						#	print  "error:",[minRed,binMethod,cutMethod,corrOption]
		if(modelType==0):
			print "best:", maxAcc, maxRank[0:10], len(maxRank), configuration
		else:
		maxAcc = 0
		maxRank = []
		configuration = []

if __name__ == '__main__':
	artificialTest()
