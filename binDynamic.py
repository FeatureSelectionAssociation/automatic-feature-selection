import numpy as np
import CorrelationMesures as cm
import util as ut

#Dynamic vs Static (Relevancy and classification)

def binarySearchBins(X, y, method=1, split=5, Debug=False):
	xbinsetList = []
	xValueList = []
	numbiny = float(len(set(y)))
	for i in range(0,X.shape[1]): #For each feature
		print "feature: ", i
		xbinset = []
		explored = []
		repeated = False #flag of repeated bin size
		bestBin = 2
		maxValue = 0
		xi = X[:,i]
		domainx = float(len(set(xi))) #domainSize
		domainx = int(pow(domainx,1.0))
		#Step 1: Initial Split
		if(split==0):
			currentBins = ut.splitSize(domainx,pow(domainx,0.5),False)
		else:
			currentBins = ut.splitSize(domainx,split,False)
		print currentBins, split
		while(not(repeated)): #Explore bins
			#Step 2: Check greater
			print "currentBins: ", currentBins
			dependencyValues = []
			for numbinx in currentBins: #Compute dependency with each bin proposed
				if(method==1):
					dependencyValues.append(round(cm.umd(xi,y,int(numbinx),int(numbiny)),2))
				else:
					dependencyValues.append(round(cm.cmd(xi,y,int(numbinx),int(numbiny)),2))
				if(numbinx in explored):
					repeated = True
				else:
					explored.append(numbinx)
			currentMaxPosition = ut.maxPosition(dependencyValues)
			currentMaxValue = dependencyValues[currentMaxPosition]
			if(currentMaxValue>maxValue):
				maxValue = currentMaxValue
				bestBin = currentBins[currentMaxPosition]
			#Step 3: Get next bins
			explored.sort()
			print "values: ", dependencyValues
			print "currentMaxPosition: ", currentMaxPosition
			print "explored: ",explored
			print "bestBin:", bestBin
			bbi = explored.index(bestBin) #best bin index
			print "bbi: ", bbi
			if(bbi>=2):
				li = round((explored[bbi]+explored[bbi-1])/2)
			else:
				print "inferior limit"
				li = round(((explored[bbi+1]+explored[bbi])/2 + 2)/2)
			if(bbi+1<len(explored)):
				ls = round((explored[bbi+1]+explored[bbi])/2)
			else:
				print "superior limit"
				ls = round((li+explored[bbi])/2)
			currentBins = [li, ls]
			print "******"
		print "maxValue: ", maxValue
		print "bestBin: ", bestBin
		xbinsetList.append(int(bestBin))
		xValueList.append(round(maxValue,2))
	print "================================================================"
	print xbinsetList
	print xValueList
	#optimalRelevancyBins(X,y,method)
	return xbinsetList

def cuadratureSearchBins(X, method=1, split=3, xjlist=False, consecutiveDepth=3, maxDepth=7, computeRepeated=False, Debug=False):
	xbinsetList = {}
	xValueList = {}
	
	if(xjlist==False):
		xjlist = range(0,X.shape[1])
	print "xjlist:",xjlist

	for i in range(0,X.shape[1]): #For each feature
		for j in xjlist:
			if(i<j):
				print "feature: ", i, ":", j
				xiBinset = []
				xjBinset = []
				xiExplored = []
				xjExplored = []				
				xiBestBin = 2
				xjBestBin = 2
				maxValue = 0
				currentDepth = 0
				totalDepth = 0
				continueFlag = True
				xi = X[:,i]
				xj = X[:,j]
				xiDomain = int(pow(len(set(xi)),1))+1 #domainSize
				xjDomain = int(pow(len(set(xj)),1))+1 #domainSize
				#Step 1: Initial Split
				if(split==0):
					xiCurrentBins = ut.splitSize(xiDomain,pow(xiDomain,0.7),False)
					xjCurrentBins = ut.splitSize(xjDomain,pow(xjDomain,0.7),False)
				else:
					xiCurrentBins = ut.splitSize(xiDomain,split,False)
					xjCurrentBins = ut.splitSize(xjDomain,split,False)
		
				while(continueFlag): #Explore bins
					print "xiCurrentBins: ", xiCurrentBins
					print "xjCurrentBins: ", xjCurrentBins
					currentDepth = currentDepth + 1
					totalDepth = totalDepth + 1					
					#Step 2: Check greater
					if((currentDepth <= consecutiveDepth) and (totalDepth <= maxDepth) ):
						dependencyValues = []
						for xiNumBin in xiCurrentBins: #Compute dependency with each bin proposed
							for xjNumBin in xjCurrentBins:
								if(method==1):
									dependencyValues.append(round(cm.umd(xi,xj,int(xiNumBin),int(xjNumBin)),2))
								else:
									dependencyValues.append(round(cm.cmd(xi,xj,int(xiNumBin),int(xjNumBin)),2))
								if(xiNumBin not in xiExplored):
									xiExplored.append(xiNumBin)
								if(xjNumBin not in xjExplored):
									xjExplored.append(xjNumBin)
						currentMaxPosition = ut.maxPosition(dependencyValues)
						xicurrentMaxPosition = int(round(currentMaxPosition/split+0.49))
						xjcurrentMaxPosition = currentMaxPosition%split
						currentMaxValue = dependencyValues[currentMaxPosition]
						maxDepth = maxDepth + 1
						print "currentPositions:", currentMaxPosition, ":", xicurrentMaxPosition, ":", xjcurrentMaxPosition
						if(currentMaxValue>maxValue):
							maxValue = currentMaxValue
							xiBestBin = xiCurrentBins[xicurrentMaxPosition]
							xjBestBin = xjCurrentBins[xjcurrentMaxPosition]
							currentDepth = 1
						print "totalDepth:currentDepth", totalDepth, ":", currentDepth
					
						#Step 3: Get next bins
						xiExplored.sort()
						xjExplored.sort()
						print "values: ", dependencyValues
						print "xiExplored: ",xiExplored
						print "xjExplored: ",xjExplored						
						print "bestBins:", xiBestBin, ":", xjBestBin
						xibb = xiExplored.index(xiBestBin) #best bin index
						xjbb = xjExplored.index(xjBestBin) #best bin index
						print "bbindexes: ", xibb, ":", xjbb
						#xibins
						if(xibb>=1):
							xili = xiExplored[xibb-1]
						else:
							print "xi inferior limit"
							xili = xiExplored[xibb]
						if(xibb+1<len(xiExplored)):
							xils = xiExplored[xibb+1]
						else:
							print "xi superior limit"
							xils = xiExplored[xibb]
						#xjbins
						if(xjbb>=1):
							xjli = xjExplored[xjbb-1]
						else:
							print "xj inferior limit"
							xjli = xjExplored[xjbb]
						if(xjbb+1<len(xjExplored)):
							xjls = xjExplored[xjbb+1]
						else:
							print "xj superior limit"
							xjls = xjExplored[xjbb]
						xiCurrentBins = ut.intervalSplit(xili,xils,split,True)
						xjCurrentBins = ut.intervalSplit(xjli,xjls,split,True)
						print "******"
					else:
						continueFlag = False
				print "maxValue: ", maxValue
				print "bestBins:", xiBestBin, ":", xjBestBin
				#xbinsetList.append([xiBestBin,xjBestBin])
				#xValueList.append(round(maxValue,2))
				xbinsetList[str(i)+":"+str(j)] = [xiBestBin,xjBestBin]
				xValueList[str(i)+":"+str(j)] = round(maxValue,2)
			print "----------------------------------------------------------------"	
	print "================================================================"
	#print xbinsetList
	#print ""
	#print xValueList
	s = sorted(xValueList, key=str.lower)
	for z in s:
		print z, ":", xValueList[z]
		#print s, ":", xValueList[z]
	return xbinsetList


def plotSurfaces(X, method=1, split=3, xjlist=False, consecutiveDepth=3, maxDepth=7, computeRepeated=False, Debug=False):
	xbinsetList = {}
	xValueList = {}
	
	if(xjlist==False):
		xjlist = range(0,X.shape[1])
	print "xjlist:",xjlist

	for i in range(2): #For each feature
		for j in range(2):
			if(i<j):
				print "feature: ", i, ":", j
				xiBinset = []
				xjBinset = []
				xiExplored = []
				xjExplored = []				
				xiBestBin = 2
				xjBestBin = 2
				maxValue = 0
				currentDepth = 0
				totalDepth = 0
				continueFlag = True
				xi = X[:,i]
				xj = X[:,j]
				xiDomain = int(pow(len(set(xi)),1))+1 #domainSize
				xjDomain = int(pow(len(set(xj)),1))+1 #domainSize
				#Step 1: Initial Split
				xiCurrentBins = ut.splitSize(xiDomain,10,False)
				xjCurrentBins = ut.splitSize(xjDomain,10,False)
				dependencyValues = []
				#indices =
				print xiCurrentBins, xjCurrentBins
				for xiNumBin in xiCurrentBins: #Compute dependency with each bin proposed
					for xjNumBin in xjCurrentBins:
						dependencyValues.append(round(cm.umd(xi,xj,int(xiNumBin),int(xjNumBin)),2))
						#print dependencyValues
				print dependencyValues
	return True

def optimalRelevancyBins(X,y,method=1):
	xbinsetList = []
	xValueList = []
	#X = np.array(data.ix[:,0:-1])
	#y = np.array(data.ix[:,-1])
	numbiny = float(len(set(y)))
	featureN = 1
	for i in range(0,X.shape[1]): #For each feature
		bestBin = 0
		maxValue = 0
		#x = np.array(data.ix[:,i])
		x = X[:,i]
		domainx = int(len(set(x)))
		domainx = int(pow(domainx,1.0))
		for numbinx in range(1,domainx):
			if(method==1):
				currentValue = cm.umd(x,y,int(numbinx),int(numbiny))
			else:
				currentValue = cm.cmd(x,y,int(numbinx),int(numbiny))
			if(currentValue>maxValue):
				maxValue = currentValue
				bestBin = numbinx
		xbinsetList.append(int(bestBin))
		xValueList.append(round(maxValue,2))
	print "================================================================"
	print xbinsetList
	print xValueList

