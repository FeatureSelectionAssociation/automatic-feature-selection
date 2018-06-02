import model as ml

def greatestDiff(weights):
	maxdiff=0
	cutpos=0
	for i in range(0,len(weights)-1):
		diff = weights[i]-weights[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	return cutpos

def monotonicValidationCut(X,y,rank,modelType=0,consecutives=5,runs=3):
	lastScore = 0
	cutpos = 0
	counter = 0
	for i in range(1,len(rank)):
		if(modelType==0):
			score = ml.clasificationJudge(X=X[:,rank[0:i]], y=y, testPerc=0.5, runs=runs)
		else:
			score = ml.regresionJudge(X=X[:,rank[0:i]], y=y, testPerc=0.5, runs=runs)

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