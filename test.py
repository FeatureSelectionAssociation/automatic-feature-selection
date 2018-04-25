import classifiers as cf
import cuts
import binDynamic as bd
import binStatic as bs
from pandas import read_csv, np
import voteSelection as vs

def artificialTest():
	#files = ['data-f1.csv','data-f2.csv','data-f3.csv','data-f4.csv','simpleCorrelations.csv','data-r50.csv','data2400-r20.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2,3,4,5],[0,1,2],[0,1,2]]
	#files = ['data-f1.csv', 'data-f2.csv','data-f3.csv','data-f4.csv','data-r50.csv','data2400-r20.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2],[0,1,2]]
	files = ['colon-cancer.csv']
	buenos = [[0,1,2,3,4,5,6]]
	

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
		#ss.append(bs.binStatic(data,3))
		weight = (vs.sumMixedCorrelation(ss))
		#print "static:",weight

		#Dynamic search
		#cr = []
		#binarySearchBinsX, y, method, split, useSteps, normalizeResult, Debug
		#cr.append(bd.binarySearchBins(X,y,0,0,2))
		#cr.append(bd.binarySearchBins(X,y,1,0,2))
		#cr.append(bd.binarySearchBins(X,y,2,0,2))
		#cr = (vs.sumMixedCorrelation(cr))
		#print "dynamic:",cr
		#bx = bd.cuadratureSearchBins(X)	
		#print bx
		
		########### Cuts ###########
		rank = cuts.getOrderRank(weight)

		print cf.getBestClassifiers(X,y)
		[X,y,cutpos] = cuts.greatestDiff(rank,weight,data)
		print cutpos, rank[0:cutpos], cf.getBestClassifiers(X,y)		
		[X,y] = cuts.monotonicValidationCut(rank,data)
		[X,y] = cuts.fullValidationCut(rank,data)
		
		i = i+1
		print "-------------------------------------\n"

artificialTest()
