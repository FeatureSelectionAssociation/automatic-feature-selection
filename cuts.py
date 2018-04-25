import numpy as np
import classifiers as cf

def getOrderRank(xlist):
	rank = [i[0] for i in sorted(enumerate(xlist), key=lambda x:x[1])]
	rank.reverse()
	#print rank
	return rank

def greatestDiff(lst):
	maxdiff=0
	cutpos=0
	for i in range(0,len(lst)-1):
		diff = lst[i]-lst[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	return cutpos

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
	#print cutpos, rank[0:cutpos]
	return [X,y,cutpos]

def fullValidationCut(rank,data):
	y = np.array(data.ix[:,-1])
	maxScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		#print rank[0:i]
		X = np.array(data.ix[:,rank[0:i]])
		score = cf.getBestClassifiers(X,y)
		if(score > maxScore):
			maxScore = score
			cutpos = i
		#print "debug full",maxScore
	X = np.array(data.ix[:,rank[0:cutpos]])
	print cutpos, rank[0:cutpos], maxScore
	return [X,y]

def monotonicValidationCut(rank,data):
	y = np.array(data.ix[:,-1])
	lastScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		X = np.array(data.ix[:,rank[0:i]])
		#print X.shape
		score = cf.getBestClassifiers(X,y)
		#print "debug monotic",lastScore,score
		if(lastScore > score):
			cutpos = i-1
			break
		lastScore = score
	X = np.array(data.ix[:,rank[0:cutpos]])
	print cutpos, rank[0:cutpos], lastScore
	return [X,y]	