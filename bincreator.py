import numpy as np
import util as ut
import math

def binsSplitBased(data, step):
	xbinsetList = []
	for i in range(0,data.shape[1]):
		f = np.array(data.ix[:,i])
		domainSize = float(len(set(f)))
		xbinset = ut.splitSize(domainSize,step)
		xbinset = xbinset[1:] #remove first element always 0
		xbinsetList.append(xbinset)
	return xbinsetList

def binsSquareBased(data, step):
	xbinsetList = []
	for i in range(0,data.shape[1]):
		f = np.array(data.ix[:,i])
		domainSize = float(len(set(f)))
		domainSize = int(round(square(domainSize),0))
		xbinset = ut.splitSize(domainSize,step)
		xbinset = xbinset[1:] #remove first element always 0
		xbinsetList.append(xbinset)
	return xbinsetList

def binsStepBased(data, v=2, sigma=0.95):
	xbinsetList = []
	asigma = 1-sigma
	for i in range(0,data.shape[1]):
		f = np.array(data.ix[:,i])
		n = len(f)
		domainSizeX = float(len(set(f)))
		domainSizeY = float(len(set(data.ix[:,-1])))
		#step = pow( (domainSizeX*domainSizeY*v*sigma) / (samples+pow(asigma,0.5) ),0.5)
		step = int(math.floor(1 / float(math.sqrt((v*sigma)/(n*math.sqrt(1-sigma))))))
		numbinX = int(math.floor(domainSizeX/step))
		stepSplit = int(round(pow(numbinX,0.5),0))
		print domainSizeX, numbinX, stepSplit
		xbinset = ut.splitSize(numbinX,stepSplit)
		xbinset = xbinset[1:] #remove first element always 0
		xbinsetList.append(xbinset)	
	return xbinsetList

def binsHistogramBased(data, v=2, sigma=0.95):
	xbinsetList = []
	for i in range(0,data.shape[1]):
		xbinset = []
		f = np.array(data.ix[:,i])
		samples = len(f)
		domainSize = float(len(set(f)))
		std = np.std(f)
		step = pow( (domainSize*v*sigma) / (samples+pow(asigma,0.5) ),0.5)
		xbinset.append(round(pow(domainSize,0.5))) #Square Root
		xbinset.append(round(np.log2(domainSize))) #Strugles
		xbinset.append(round(2*pow(domainSize,0.3333))) #Rice
		xbinset.append(round((3.5*std)/pow(domainSize,0.3333))) #Scott normal
		xbinset.append(int(math.floor(step))) #v and sigma based		
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



