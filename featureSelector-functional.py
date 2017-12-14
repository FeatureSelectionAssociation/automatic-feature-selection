import numpy as np
from CorrelationMesures import *
from pandas import *
#"best=good in this time" 

def maxlist(a,b):
	result = []
	for i in range(0,len(a)):
		result.append(max(a[i],b[i]))
	return result

def getOrderRank(xlist):
	rank = [i[0] for i in sorted(enumerate(xlist), key=lambda x:x[1])]
	rank.reverse()
	print rank

def printresult(PMDbest,PMD2best,labelcol):
	for i in range(0,len(PMDbest)):
		print i,labelcol,":",PMDbest[i],PMD2best[i]

def get_bestcorlab(xbinset,ybinset,filename, cols, labelcol):
	PMDbest = [0] * (cols-1)
	PMD2best = [0] * (cols-1)
	for numBinx in xbinset:
		for numBiny in ybinset:
			PMD, PMD2 = get_corrlab(numBinx, numBiny, filename, cols, labelcol)
			PMDbest = maxlist(PMDbest,PMD)
			PMD2best = maxlist(PMD2best,PMD2)
			#print numBinx,numBiny,":",PMD,PMD2
	#print PMDbest,PMD2best
	printresult(PMDbest,PMD2best,labelcol)
	getOrderRank(PMDbest)
	getOrderRank(PMD2best)
	return 

def get_corrlab(numBinx,numBiny,filename, cols, labelcol):	
	data = read_csv(filename)
	y = np.array(data.ix[:,labelcol])
	PMD = []
	PMD2 = []
	for i in range(0,cols):
		if(i!=labelcol):
			x = np.array(data.ix[:,i])
			PMD.append(round(propuesta_mutual_dependency(x, y, numBinx, numBiny),3))
			PMD2.append(round(propuesta2_mutual_dependency(x, y, numBinx, numBiny),3))
	return PMD, PMD2
	
xbinset = [2,3,4,5]
ybinset = [2,3,4,5]

#Parece ser que el correr 

#print "ejemplo.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\ejemplo.csv', 6, 5)
#print "data.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\data.csv', 4, 3)
#print "data-fs.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\data-fs.csv', 6, 5)
#print "data-fsfe.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\data-fsfe.csv', 7, 6)
#print "data-r20.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\data-r20.csv', 24, 23)
#print "data-r50.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\data-r50.csv', 54, 53)
#print "colon-cancer.csv"
#get_bestcorlab(xbinset, ybinset, 'Data\colon-cancer.csv', 2001, 2000)
print "colon-cancer-fs.csv"
get_bestcorlab(xbinset, ybinset, 'Data\colon-cancer-fs.csv', 11, 10)
print "colon-cancer-fs2.csv"
get_bestcorlab(xbinset, ybinset, 'Data\colon-cancer-fs2.csv', 11, 10)

