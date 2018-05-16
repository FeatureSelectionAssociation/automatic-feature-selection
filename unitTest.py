from pandas import read_csv, np
import util as ut
import cuts
import binSelection as bs
import classifiers as cf
import parallel as p
import time

def artificialTest():
	#files = ['data-f1.csv','data-f2.csv','data-f3.csv','data1000-f4.csv','simpleCorrelations.csv','data-r50.csv','data2400-r20.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2,3,4,5],[0,1,2],[0,1,2]]
	#files = ['data-f1.csv', 'data-f2.csv','data-f3.csv','data-f4.csv','data-r50.csv','data2400-r20.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2],[0,1,2]]
	#files = ['real/leu.csv']
	#buenos = [[0,1,2,3,4,5,6]]
	files = ['data1000-f4.csv']
	buenos = [[0,1,3,2]]
		
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
		#'''
		startTime = time.time()
		weights = bs.binStatic(X,y,0)
		endTime = time.time()
		print "Serial static " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:3]
		startTime = time.time()
		weights = p.binStatic(X,y,0)
		endTime = time.time()
		print "Parallel static " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:3]
		#weights = ut.sumMixedCorrelation([bs.binStatic(X,y,0),bs.binStatic(X,y,1)])		
		#print "static:",weight
		#'''

		#Dynamic search
		startTime = time.time()
		weights = bs.binarySearchBins(X,y,2,0,2)
		endTime = time.time()
		print "Serial dynamic " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:3]
		startTime = time.time()
		weights = p.binarySearchBins(X,y,0,2,0,2)
		endTime = time.time()
		print "Parallel dynamic " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:3]
		#weights = ut.sumMixedCorrelation([bs.binarySearchBins(X,y,0,0,2),bs.binarySearchBins(X,y,1,0,2)])
		#print "dyniamic:",weights

		

		########### Cuts ###########
		#'''
		print "\nCuts:"
		rank = ut.getOrderRank(weights)
		print "rank:",rank[0:5]
		#print cf.getBestClassifiers(X,y)
		cutpos = cuts.greatestDiff(rank)
		print cutpos
		#print cutpos, rank[0:cutpos], cf.getBestClassifiers(X,y)		
		#cutpos = cuts.monotonicValidationCut(X,y,rank)
		#[X,y] = cuts.fullValidationCut(rank,data)
		i = i+1
		print "-------------------------------------\n"
		#'''
if __name__ == '__main__':
	artificialTest()
