from pandas import read_csv, np
import util as ut
import cuts
import binSelection as bs
import classifiers as cf
import parallel as p
import time

def artificialTest():
	#files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv','data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv','data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2],[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]	
	files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv']
	buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]
	#files = ['data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]
	#files = ['data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]
	
	#files = ['regression/reg1000-f1.csv']
	#buenos = [[0,1,2,3,4,5]]
	#files = ['real/leu.csv']
	#buenos = [[0,1,2,3,4,5,6]]
	#files = ['data20000-f3.csv']
	#buenos = [[0,1,3,2]]
		
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
		weights = bs.binStatic(X,y,2)
		endTime = time.time()
		print "Serial static " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:5]
		startTime = time.time()
		weights = p.binStatic(X,y,0,2)
		endTime = time.time()
		print "Parallel static " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:5]
		#weights = ut.sumMixedCorrelation([bs.binStatic(X,y,0),bs.binStatic(X,y,1)])		
		#print "static:",weight
		#'''

		#Dynamic search
		#'''
		startTime = time.time()
		weights = bs.binarySearchBins(X,y,2,0,2)
		endTime = time.time()
		print "Serial dynamic " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:5]
		startTime = time.time()
		weights = p.binarySearchBins(X,y,0,2,0,2)
		endTime = time.time()
		print "Parallel dynamic " + str(round(endTime-startTime,3)) + " seconds to complete"
		print weights[0:5]
		#weights = ut.sumMixedCorrelation([bs.binarySearchBins(X,y,0,0,2),bs.binarySearchBins(X,y,1,0,2)])
		#print "dyniamic:",weights
		#'''
		

		########### Cuts ###########
		#'''
		print "\nCuts:"
		rank = ut.getOrderRank(weights)
		print "rank:",rank[0:5]
		print cf.getBestClassifiers(X,y)
		cutpos = cuts.greatestDiff(weights)
		#print cutpos
		print cutpos, rank[0:cutpos], cf.getBestClassifiers(X[:,rank[0:cutpos]],y)		
		cutpos = cuts.monotonicValidationCut(X,y,rank)
		print cutpos, rank[0:cutpos], cf.getBestClassifiers(X[:,rank[0:cutpos]],y)
		cutpos = cuts.fullValidationCut(X,y,rank)
		print cutpos, rank[0:cutpos], cf.getBestClassifiers(X[:,rank[0:cutpos]],y)
		i = i+1
		print "-------------------------------------\n"
		#'''
if __name__ == '__main__':
	artificialTest()
