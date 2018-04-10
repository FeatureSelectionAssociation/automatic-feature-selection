import numpy as np

#Get dependency of x_i from y 
def get_corrlab(numBinx,numBiny,data,cols):	
	PMD = []
	PMD2 = []
	y = np.array(data.ix[:,-1])
	for i in range(0,cols):
		x = np.array(data.ix[:,i])
		PMD.append(round(propuesta_mutual_dependency(x, y, numBinx, numBiny),3))
		PMD2.append(round(propuesta2_mutual_dependency(x, y, numBinx, numBiny),3))
	return PMD, PMD2

#Get "Best" dependency of x_i from y  
def get_bestcorlab(xbinset,ybinset,data):
	cols = data.shape[1]-1
	PMDbest = [0] * (cols)
	PMD2best = [0] * (cols)
	for numBinx in xbinset:
		for numBiny in ybinset:
			PMD, PMD2 = get_corrlab(numBinx, numBiny, data, cols)
			PMDbest = maxlist(PMDbest,PMD)
			PMD2best = maxlist(PMD2best,PMD2)
			#print numBinx,numBiny,":",PMD,PMD2
			#print numBinx,numBiny
			#getOrderRank(PMDbest)
			#getOrderRank(PMD2best)
	#print PMDbest,PMD2best
	#printresult(PMDbest,PMD2best,cols)
	getOrderRank(PMDbest)
	getOrderRank(PMD2best)
	print PMDbest
	print PMD2best
	return [PMDbest, PMD2best]

def get_corrlabDynamic(xbinset,ybinset,x,y):	
	PMD = []
	PMD2 = []
	for numBinx in xbinset:
		for numBiny in ybinset:
			#print numBinx
			#print numBiny
			PMD.append(round(propuesta_mutual_dependency(x, y, numBinx, numBiny),3))
			PMD2.append(round(propuesta2_mutual_dependency(x, y, numBinx, numBiny),3))
	#print PMD, PMD2
	return max(PMD), max(PMD2)

def get_bestcorlabDynamic(data):
	cols = data.shape[1]-1
	PMDbest = [0] * (cols)
	PMD2best = [0] * (cols)
	binList = bc.getDynamicBins(data)
	#print binList
	y = np.array(data.ix[:,-1])
	for i in range(0,cols):
		x = np.array(data.ix[:,i])
		xbinset = binList[i]
		ybinset = binList[cols]
		PMD, PMD2 = get_corrlabDynamic(xbinset, ybinset, x,y)
		PMDbest[i] = PMD
		PMD2best[i] = PMD2
		#print i,xbinset,ybinset,PMD,PMD2
	#print PMDbest
	#print PMD2best
	features = getOrderRank(PMDbest)
	getOrderRank(PMD2best)
	#print PMDbest,PMD2best
	PMDbest.sort()
	PMDbest.reverse()
	#print PMDbest
	#nf = cut.greatestDiff(PMDbest)
	#sFeatures = features[0:nf]
	#print sFeatures
	#newX = np.array(data.ix[:,sFeatures])
	#return [newX, y]
	return [features,PMDbest]