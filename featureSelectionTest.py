import classifiers as cf
import featureSelection as fs
from pandas import read_csv, np
import time
def artificialTest():
	#Artifial Datasets
	files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv','data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv','data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv','data1000-f1-r500.csv','data5000-f1-r500.csv','data20000-f1-r500.csv']
	buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1,2,3,4,5,6,13,14],[0,1,2,3,4,5,6,13,14],[0,1,2,3,4,5,6,13,14]]	
	#Real Datasets
	#files = ['real/sonar_scale.csv', 'real/splice_scale.csv', 'real/colon-cancer.csv', 'real/leu.csv', 'real/duke.csv', 'real/BH20000.csv', 'real/madelon-test.csv']
	#buenos = [['?'],['?'],['?'],['?'],['?'],['?'],['?']]
	i=0
	verboseClassifiers = True
	for f in files:
		maxAcc = 0
		maxRank = []
		configuration = []	
		filepath = 'Data/'+f		
		data = read_csv(filepath)
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		print filepath, buenos[i]
		startTime = time.time()
		acc = cf.clasificationJudge(X,y)
		endTime = time.time()
		print "original:", acc, X.shape[1], str(round(endTime-startTime,3))+"s"
		for minRed in range(0,2):
			for binMethod in range(0,2):
				for cutMethod in range(0,3):
					for corrOption in range(0,6):
						try:
							startTime = time.time()
							rank = fs.featureSelection(X=X,y=y, processes=0, corrOption=corrOption, binMethod=binMethod, cutMethod=cutMethod, minRed=minRed, debug=False)							
							endTime = time.time()
							timefs = round(endTime-startTime,3)
							X = np.array(data.ix[:,rank])
							startTime = time.time()
							acc = cf.clasificationJudge(X,y)
							endTime = time.time()
							timecf = round(endTime-startTime,3)
							print minRed,binMethod, cutMethod, corrOption, acc, timefs, timecf, len(rank), rank[0:5]			
							if(acc>maxAcc):
								maxAcc = acc
								maxRank = rank
								configuration = [minRed,binMethod,cutMethod,corrOption]
							X = np.array(data.ix[:,0:-1])
						except Exception as inst:
							X = np.array(data.ix[:,0:-1])
							print  "error:",[minRed,binMethod,cutMethod,corrOption]
		print "best:", maxAcc, maxRank[0:10], len(maxRank), configuration
		maxAcc = 0
		maxRank = []
		configuration = []

if __name__ == '__main__':
	artificialTest()
