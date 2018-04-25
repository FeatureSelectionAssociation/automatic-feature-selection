import numpy as np
import math
import step as st
import CorrelationMesures as cm

def binStatic(data, method=1):
	binSetList = []
	binSetListResult = []
	binValueResult = []
	for i in range(0,data.shape[1]):
		binSet = []
		f = np.array(data.ix[:,i])
		N = len(f)
		domainSize = float(len(set(f)))
		std = np.std(f)
		binSet.append(st.computeStepV2(domainSize, N))
		binSet.append(round(pow(domainSize,0.5))) #Square Root
		binSet.append(round(np.log2(domainSize))) #Strugles
		binSet.append(round(2*pow(domainSize,0.3333))) #Rice
		binSet.append(round((3.5*std)/pow(domainSize,0.3333))) #Scott normal
		for i in range(0,len(binSet)):
			if(domainSize<(pow(N,0.5)/2)):
				binSet[i] = domainSize
			if(binSet[i] < 2):
				binSet[i] = 2
			if(binSet[i] > binSet[0]):
				binSet[i] = binSet[0]
		binSet = map(int,binSet)
		binSet = set(binSet)
		binSet = list(binSet)
		binSetList.append(binSet)
	result =  computeValue(data,binSetList, method)[0]
	return result

def computeValue(data, binSetList, method):
	y = np.array(data.ix[:,-1])
	binValueResult = []
	binSetResult = []
	for i in range(0,data.shape[1]-1):
		xi = np.array(data.ix[:,i])	
		binValue = 0
		maxValue = 0
		binResult = []
		for numbinx in binSetList[i]:
			for numbiny in binSetList[-1]:
				if(method==0):
					binValue = round(cm.umdv(xi,y,int(numbinx),int(numbiny)),2)
				elif(method==1):
					binValue = round(cm.cmdv(xi,y,int(numbinx),int(numbiny)),2)
				elif(method==2):
					binValue = round(cm.ucmdv(xi,y,int(numbinx),int(numbiny)),2)
				elif(method==3):
					binValue = round(cm.MIC(xi,y),2)
				if(binValue>maxValue):
					maxValue=binValue
					binResult = [numbinx,numbiny]
		binValueResult.append(maxValue)
		binSetResult.append(binResult)
	return [binValueResult, binSetResult]
