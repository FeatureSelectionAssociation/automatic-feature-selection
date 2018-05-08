import math

def maxlist(a,b):
	result = []
	for i in range(0,len(a)):
		result.append(max(a[i],b[i]))
	return result

def getOrderRank(xlist):
	rank = [i[0] for i in sorted(enumerate(xlist), key=lambda x:x[1])]
	rank.reverse()
	return rank

def splitSize(size,split, zero=True):
	split = int(split)
	bins = [size]*split
	binsSize = float(size)/split
	for i in range(0,split):
		bins[i] = int(round(binsSize*(i)))
		if(bins[i]==1):
			bins[i]=2
	bins.append(size)
	if(zero==False):
		bins.remove(0)
	bins = list(set(bins))
	bins.sort()
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

def normalize(arr):
	maxValue = max(arr)
	arr[:] = [round(x / maxValue,2) for x in arr]
	return arr

def computeStep(rangeX, rangeY, N, v=2, sigma=0.95): #useSteps = 0
    num = rangeX*rangeY*v*sigma
    den = N*pow((1-sigma),0.5)
    step = pow(num/den,0.5)
    resultX = int(math.floor(rangeX / step))
    resultY = int(math.floor(rangeY / step))
    if(resultX<=2):
        resultX=2
    if(resultY<=2):
        resultY=2
    return [resultX,resultY]

def computeStepNormalized(N, v=2, sigma=0.95): #useSteps = 2
    return int(math.floor(1 / float(math.sqrt((v*sigma)/(N*math.sqrt(1-sigma))))))

def computeStepV2(rangeData, N, v=2, sigma=0.95): #useSteps = 2
    if(rangeData>(pow(N,0.5)/2)):
        num = rangeData*v*sigma
        den = N*pow((1-sigma),0.5)
        step = pow(num/den,0.5)
        result = int(math.floor(rangeData / step))
    else:
        result = rangeData
    return int(result)