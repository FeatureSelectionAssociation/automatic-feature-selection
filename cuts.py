import numpy as np
import classifiers as cf

def greatestDiff(lst):
	maxdiff=0
	cutpos=0
	for i in range(0,len(lst)-1):
		diff = lst[i]-lst[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	return cutpos

def fullValidationCut(X,y,rank):
	maxScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		score = cf.getBestClassifiers(X,y)
		if(score > maxScore):
			maxScore = score
			cutpos = i
	#X = np.array(data.ix[:,rank[0:cutpos]])
	#print cutpos, rank[0:cutpos], maxScore
	#return [X,y,cutpos]
	return cutpos

def monotonicValidationCut(X,y,rank, consecutives=3):
	lastScore = 0
	cutpos = 0
	counter = 0
	for i in range(1,len(rank)):
		#print X[:,rank[0:i]].shape
		score = cf.getBestClassifiers(X[:,rank[0:i]],y)
		#print lastScore,score
		if(lastScore > score):
			counter = counter + 1
			if(counter>=consecutives):
				cutpos = i-consecutives			
				break
		else:
			counter = 0
			lastScore = score
	#X = np.array(data.ix[:,rank[0:cutpos]])
	#print cutpos, rank[0:cutpos], lastScore
	#return [X,y,cutpos]
	return cutpos

def monotonicValidationCutOr(X,y,rank):
	lastScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		#print X[:,rank[0:i]].shape
		score = cf.getBestClassifiers(X[:,rank[0:i]],y)
		if(lastScore > score):
			cutpos = i-1
			break
		lastScore = score
	#X = np.array(data.ix[:,rank[0:cutpos]])
	#print cutpos, rank[0:cutpos], lastScore
	#return [X,y,cutpos]
	return cutpos