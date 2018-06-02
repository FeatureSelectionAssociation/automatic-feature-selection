import classifiers as cf

def greatestDiff(weights):
	maxdiff=0
	cutpos=0
	for i in range(0,len(weights)-1):
		diff = weights[i]-weights[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	return cutpos

def monotonicValidationCut(X,y,rank,consecutives=5):
	lastScore = 0
	cutpos = 0
	counter = 0
	for i in range(1,len(rank)):
		score = cf.clasificationJudge(X[:,rank[0:i]],y)
		if(lastScore >= score):
			counter = counter + 1
			if(counter>=consecutives):
				cutpos = i-consecutives			
				break
		else:
			counter = 0
			lastScore = score
			cutpos = i
	if(cutpos<=0):
		cutpos=1
	return cutpos

def fullValidationCut(X,y,rank):
	maxScore = 0
	cutpos = 0
	for i in range(1,len(rank)):
		score = cf.clasificationJudge(X[:,rank[0:i]],y)
		if(score > maxScore):
			maxScore = score
			cutpos = i
	return cutpos