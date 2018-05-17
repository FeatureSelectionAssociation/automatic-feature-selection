from pandas import read_csv, np
import util as ut
import cuts
import binSelection as bs
import classifiers as cf
import parallel as p
import time

def artificialTest():
	#Syntentic classification datasets
	#files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv','data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv','data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2],[0,1],[0,1],[0,1,3,2],[0,1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]	
	#files = ['data1000-f1.csv', 'data1000-f2.csv','data1000-f3.csv','data1000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2]]
	#files = ['data5000-f1.csv', 'data5000-f2.csv','data5000-f3.csv','data5000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2]]
	#files = ['data20000-f1.csv', 'data20000-f2.csv','data20000-f3.csv','data20000-f4.csv']
	#buenos = [[0,1,2,3,4,5,6,13,14],[0,1,8,9],[0,1,6,7],[0,1,3,2]]
	
	#Syntetic Regression datasets
	#files = ['regression/reg1000-f1.csv']
	
	#Real Datasets
	#buenos = [[0,1,2,3,4,5]]
	#files = ['real/leu.csv']
	
	#Current Testing datasets
	#buenos = [[0,1,2,3,4,5,6]]
	#files = ['data1000-f1-r500.csv']
	#buenos = [[0,1,3,2]]	
	files = ['data5000-f1.csv']
	buenos = [[0,1,3,2]]	
	
	i=0
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
		print "Serial static " + str(round(endTime-startTime,3)) + " seconds."
		print "weights:", weights[0:20]
		startTime = time.time()
		weights = p.binStatic(X,y,0,2)
		endTime = time.time()
		print "Parallel static " + str(round(endTime-startTime,3)) + " seconds."
		print "weights:", weights[0:20]
		#weights = ut.sumMixedCorrelation([bs.binStatic(X,y,0),bs.binStatic(X,y,1)])		
		#print "Combined Static:",weight
		#'''

		#Dynamic search
		#'''
		startTime = time.time()
		weights = bs.binarySearchBins(X,y,2,0,2)
		endTime = time.time()
		print "Serial dynamic " + str(round(endTime-startTime,3)) + " seconds."
		print "weights:", weights[0:20]
		startTime = time.time()
		weights = p.binarySearchBins(X,y,0,2,0,2)
		endTime = time.time()
		print "Parallel dynamic " + str(round(endTime-startTime,3)) + " seconds."
		print "weights:", weights[0:20]
		#weights = ut.sumMixedCorrelation([bs.binarySearchBins(X,y,0,0,2),bs.binarySearchBins(X,y,1,0,2)])
		#print "Combined Dyniamic:",weights
		#'''
		

		########### Cuts ###########
		
		print "\nCuts:"
		rank = ut.getOrderRank(weights)
		print "rank:",rank[0:20]
		
		#'''
		startTime = time.time()
		print "Full features Accurracy:", cf.getBestClassifiers(X,y)
		endTime = time.time()
		print "Full classification time: " + str(round(endTime-startTime,3)) + " seconds."
		
		startTime = time.time()
		cutpos1 = cuts.greatestDiff(weights)
		endTime = time.time()
		print "\nCut GreatestDiff time: " + str(round(endTime-startTime,3)) + " seconds."
		startTime = time.time()
		print "GreatestDiff Accurracy:", cf.getBestClassifiers(X[:,rank[0:cutpos1]],y), " #features:", cutpos1 		
		endTime = time.time()
		print "Classification GreatestDiff time: " + str(round(endTime-startTime,3)) + " seconds."
		
		startTime = time.time()
		cutpos2 = cuts.monotonicValidationCut(X,y,rank)
		endTime = time.time()
		print "\nCut MonotonicValidationCut time: " + str(round(endTime-startTime,3)) + " seconds."
		startTime = time.time()
		print "MonotonicValidation Accurracy:", cf.getBestClassifiers(X[:,rank[0:cutpos2]],y), " #features:", cutpos2 
		endTime = time.time()
		print "Classification MonotonicValidationCut time: " + str(round(endTime-startTime,3)) + " seconds."
		'''
		'''
		startTime = time.time()
		cutpos3 = cuts.monotonicValidationCut(X,y,rank,10)
		#cutpos3 = cuts.fullValidationCut(X,y,rank)
		endTime = time.time()
		print "Cut FullValidationCut time: " + str(round(endTime-startTime,3)) + " seconds."
		startTime = time.time()
		print "FullValidationCut Accurracy:", cf.getBestClassifiers(X[:,rank[0:cutpos3]],y), " #features:", cutpos3 
		endTime = time.time()
		print "Classification FullValidationCut time: " + str(round(endTime-startTime,3)) + " seconds."
		#'''
		
		#Removing redundant
		originalRank = list(rank)
		print "\nFinding redundant features:"
		#'''
		startTime = time.time()
		rank =  set(bs.removeRedundant(X, rank))
		print "Serial mode"
		print "Original Rank:", originalRank
		print "Not redundant:",rank
		print "Redundant:",set(originalRank).difference(set(rank))
		endTime = time.time()
		print "Time finding redundant: " + str(round(endTime-startTime,3)) + " seconds."
		#'''
		startTime = time.time()
		rank = list(originalRank)
		rank =  set(p.parallelRemoveRedundant(X,rank))		
		print "Parallel mode"
		print "Original Rank:", originalRank
		print "Not redundant:",rank
		print "Redundant:", set(originalRank).difference(set(rank))
		endTime = time.time()
		print "Time finding redundant: " + str(round(endTime-startTime,3)) + " seconds."
		#'''
		
		i = i+1
		print "-------------------------------------\n"
		#'''
if __name__ == '__main__':
	artificialTest()
