import classifiers as cf
import featureSelection as fs
import binSelection as bs
from pandas import read_csv, np
def artificialTest():
	#files = ['data-f1.csv','data-f2.csv','data-f3.csv','data-f4.csv','data-r50.csv','data2400-r20.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2],[0,1,2]]
	files = ['sonar_scale.csv', 'splice_scale.csv', 'colon-cancer.csv', 'leu.csv', 'duke.csv', 'BH20000.csv', 'madelon-test.csv']
	buenos = [['?'],['?'],['?'],['?'],['?'],['?'],['?']]
		

	i=0
	verboseClassifiers = True
	for f in files:
		maxAcc = 0
		maxRank = []
		configuration = []
		#filepath = 'Data/'+f		
		filepath = 'Data/real/'+f		
		
		data = read_csv(filepath)
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		print filepath, buenos[i]
		print "original:",cf.getBestClassifiers(X,y)
		for binMethod in range(0,2):
			for cutMethod in range(0,2):
				for corrOption in range(0,6):
					#print corrOption
					try:
						rank = fs.featureSelection(X, y, corrOption=corrOption, binMethod=binMethod, cutMethod=cutMethod, minRed=True)
						X = np.array(data.ix[:,rank])
						acc = cf.getBestClassifiers(X,y)
						print binMethod, cutMethod, corrOption, acc, len(rank), rank[0:3]			
						if(acc>maxAcc):
							maxAcc = acc
							maxRank = rank
							configuration = [binMethod,cutMethod,corrOption]
						X = np.array(data.ix[:,0:-1])

					except Exception as inst:
						X = np.array(data.ix[:,0:-1])
						#print type(inst)
						#print inst.args
				#print "-----"
			#print "*****"
		#print "#####"
		print maxAcc, maxRank, configuration, len(maxRank)
		maxAcc = 0
		maxRank = []
		configuration = []

artificialTest()
