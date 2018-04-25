#import featureSelector as fs
import classifiers as cf
import cuts
import binDynamic as bd
import binStatic as bs
from pandas import *
import plots as pt
import measureMixer as mm

def artificialTest():
	files = ['data-f1.csv','data-f2.csv','data-f3.csv','data-f4.csv','simpleCorrelations.csv','data-r50.csv','data2400-r20.csv']
	buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2,3,4,5],[0,1,2],[0,1,2]]
	#files = ['data-f1.csv', 'data-f2.csv','data-f3.csv','data-f4.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]
	#files = ['data-f1.csv']
	#buenos = [[0,1,2,3,4,5,6]]
	

	i=0
	verboseClassifiers = True
	for f in files:
		filename = 'Data/'+f
		
		########### Separate Data ###########
		print filename, buenos[i]
		data = read_csv(filename)
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		
		########### Search ###########
		#Static search
		ss = []
		ss.append(bs.binStatic(data,0))
		ss.append(bs.binStatic(data,1))
		ss.append(bs.binStatic(data,2))
		ss = (mm.sumMixedCorrelation(ss))
		print "static:",ss

		#Dynamic search
		cr = []
		#binarySearchBinsX, y, method, split, useSteps, normalizeResult, Debug
		cr.append(bd.binarySearchBins(X,y,0,0,2))
		cr.append(bd.binarySearchBins(X,y,1,0,2))
		cr.append(bd.binarySearchBins(X,y,2,0,2))
		
		
		cr = (mm.sumMixedCorrelation(cr))
		print "dynamic:",cr
		#bx = bd.cuadratureSearchBins(X)	
		#print bx
		
		########### Cuts ###########
		#[X,y] = cuts.greatestDiff(rank,weight,data)
		#[X,y] = cuts.monotonicValidationCut(rank,weight,data)
		#[X,y] = cuts.fullValidationCut(rank,weight,data)
		
		########### Classify ###########
		#print cf.getBestClassifiers(X,y,verboseClassifiers)
		i = i+1
		print "-------------------------------------\n"

artificialTest()
