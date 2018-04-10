def maxlist(a,b):
	result = []
	for i in range(0,len(a)):
		result.append(max(a[i],b[i]))
	return result

def getOrderRank(xlist):
	rank = [i[0] for i in sorted(enumerate(xlist), key=lambda x:x[1])]
	rank.reverse()
	#print rank
	return rank

def printresult(PMDbest,PMD2best,labelcol):
	for i in range(0,len(PMDbest)):
		print i,labelcol,":",PMDbest[i],PMD2best[i]

def splitSize(size,split, zero=True):
	split = int(split)
	bins = [size]*split
	binsSize = float(size)/split
	for i in range(0,split):
		bins[i] = int(round(binsSize*(i)))
	bins.append(size)
	if(zero==False):
		bins.remove(0)
	return bins

def intervalSplit(infLim,supLim,split=2,limitIncluded=False):
	bins = []
	print "[",infLim, ",", supLim, "]"
	if(limitIncluded):
		stepSize = (supLim-infLim)/(split-1.0)
		addValue = infLim
		while(addValue <= supLim):
			bins.append(int(round(addValue)))
			addValue = addValue + stepSize
			#print addValue
	else:
		stepSize = (supLim-infLim)/(split+1.0)
		addValue = infLim
		while(addValue + stepSize < supLim):
			addValue = addValue + stepSize
			#print addValue
			bins.append(int(round(addValue)))
	#bins = list(set(bins))
	return bins

def maxPosition(l):
	position = 0
	maxVal = 0
	for i in range(len(l)):
		if(l[i]>maxVal):
			maxVal = l[i]
			position = i
	return position
