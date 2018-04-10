import numpy as np
import util as ut

def binsSplitBased(data, step):
	xbinsetList = []
	for i in range(0,data.shape[1]):
		domainSize = float(len(set(f)))
		xbinset = ut.splitSize(domainSize,step)
		xbinset = xbinset[1:] #remove first element always 0
		xbinsetList.append(xbinset)
	return xbinsetList

def binsSquareBased(data, step):
	xbinsetList = []
	for i in range(0,data.shape[1]):
		domainSize = float(len(set(f)))
		domainSize = int(round(square(domainSize),0))
		xbinset = ut.splitSize(domainSize,step)
		xbinset = xbinset[1:] #remove first element always 0
		xbinsetList.append(xbinset)
	return xbinsetList

def binsHistogramBased(data):
	xbinsetList = []
	for i in range(0,data.shape[1]):
		xbinset = []
		f = np.array(data.ix[:,i])
		samples = len(f)
		domainSize = float(len(set(f)))
		std = np.std(f)
		xbinset.append(round(pow(domainSize,0.5))) #Square Root
		xbinset.append(round(np.log2(domainSize))) #Strugles
		xbinset.append(round(2*pow(domainSize,0.3333))) #Rice
		xbinset.append(round((3.5*std)/pow(domainSize,0.3333))) #Scott normal
		for i in range(0,len(xbinset)):
			if(domainSize<50):
				xbinset[i] = domainSize
			else:
				if(xbinset[i]>domainSize/5 and domainSize>50):
					xbinset[i] = domainSize/5
				if(xbinset[i]<=1):
					xbinset[i] = 2
		xbinset = map(int,xbinset)
		xbinset = set(xbinset)
		xbinset = list(xbinset)
		xbinsetList.append(xbinset)				
	return xbinsetList
