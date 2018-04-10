#import featureSelector as fs
import classifiers as cf
import cuts
import binDynamic as bd
from pandas import *
import plots as pt

def artificialTest():
	files = ['simpleCorrelations.csv']
	buenos = [[1,2,3,4,5,6]]
	i=0
	for f in files:
		filename = 'Data/'+f
		print filename, buenos[i]
		data = read_csv(filename)
		X = np.array(data.ix[:,0:-1])
		#X = np.array(data.ix[:])
		y = np.array(data.ix[:,-1])
		print X.shape
		print y.shape
		#bd.binarySearchBins(X,y,1,5)
		bd.cuadratureSearchBins(X)
		#X = np.array(data.ix[:,0:-1])
		#y = np.array(data.ix[:,-1])
		#print cf.getBestClassifiers(X,y,verboseClassifiers)
		##print "static"
		##fs.get_bestcorlab(xbinset, ybinset, data)
		##print "dynamic"
		#[rank,weight] = fs.get_bestcorlabDynamic(data)
		#[X,y] = cuts.greatestDiff(rank,weight,data)
		#print cf.getBestClassifiers(X,y,verboseClassifiers)
		#[X,y] = cuts.monotonicValidationCut(rank,weight,data)
		#print cf.getBestClassifiers(X,y,verboseClassifiers)
		##[X,y] = cuts.fullValidationCut(rank,weight,data)
		##print cf.getBestClassifiers(X,y,verboseClassifiers)
		i = i+1
		print "-------------------------------------\n"

artificialTest()
