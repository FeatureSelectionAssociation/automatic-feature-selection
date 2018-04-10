import numpy as np
import classifiers as cf

def greatestDiff(rank,weight,data):
	maxdiff=0
	cutpos=0
	for i in range(0,len(weight)-1):
		diff = weight[i]-weight[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	X = np.array(data.ix[:,rank[0:cutpos]])
	y = np.array(data.ix[:,-1])
	print cutpos, rank[0:cutpos]
	return [X,y]

def fullValidationCut(rank,weight,data):
	y = np.array(data.ix[:,-1])
	maxScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		X = np.array(data.ix[:,rank[0:i]])
		score = cf.getBestClassifiers(X,y)
		if(score > maxScore):
			maxScore = score
			cutpos = i
	X = np.array(data.ix[:,rank[0:cutpos]])
	print cutpos, rank[0:cutpos]
	return [X,y]

def monotonicValidationCut(rank,weight,data):
	y = np.array(data.ix[:,-1])
	lastScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		X = np.array(data.ix[:,rank[0:i]])
		score = cf.getBestClassifiers(X,y)
		#print "debug",lastScore,score
		if(lastScore > score):
			cutpos = i-1
			break
		lastScore = score
	X = np.array(data.ix[:,rank[0:cutpos]])
	print cutpos, rank[0:cutpos]
	return [X,y]	