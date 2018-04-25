import numpy as np
from correlationMesures import *
import bincreator as bc
import cut as cut
      
def maxlist(a,b):
	result = []
	for i in range(0,len(a)):
		result.append(max(a[i],b[i]))
	return result

def getOrderRank(xlist):
	rank = [i[0] for i in sorted(enumerate(xlist), key=lambda x:x[1])]
	rank.reverse()
	print rank
	return rank

def printresult(PMDbest,PMD2best,labelcol):
	for i in range(0,len(PMDbest)):
		print i,labelcol,":",PMDbest[i],PMD2best[i]

def get_corrlab(numBinx,numBiny,data,cols):	
	PMD = []
	PMD2 = []
	y = np.array(data.ix[:,-1])
	for i in range(0,cols):
		x = np.array(data.ix[:,i])
		PMD.append(round(propuesta_mutual_dependency(x, y, numBinx, numBiny),3))
		PMD2.append(round(propuesta2_mutual_dependency(x, y, numBinx, numBiny),3))
	return PMD, PMD2

