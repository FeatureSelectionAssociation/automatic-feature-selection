import util as ut
import binSelection as bs
import cuts
from pandas import read_csv, np
import CorrelationMesures as cm
import parallel as p

#binMethod 0 = Relevancy with total static bin selection
#binMethod 1 = Relevancy with dynamic bin selection
#corrOption 0 = umdv
#corrOption 1 = cmdv
#corrOption 2 = (umd+cmd)/2
#corrOption 3 = MIC
#corrOption 4 = vote (umdv + cmdv)
#corrOption 5 = vote (umdv + cmdv + mic)
#cutMethod 0 = greatestDiff2
#cutMethod 1 = monotonicValidationCut
#cutMethod 2 = fullValidationCut
def featureSelection(X,y, corrOption=4, binMethod=0, cutMethod=1, minRed=0, debug=True):
	if(corrOption<=3):
		corrMethod = corrOption
	elif(corrOption==4):
		corrOption = [0,1]
	elif(corrOption==5):
		corrOption = [0,1,3]
	wlist = []
	if(corrOption<=3):
		if(binMethod==0):
			#weights = bs.binStatic(X,y,corrMethod)
			weights = p.binStatic(X,y,0,corrMethod)
		elif(binMethod==1):
			#weights = bs.binarySearchBins(X,y,corrMethod,0,2)
			weights = p.binarySearchBins(X,y,0,corrMethod,0,2)
	else:
		for corrMethod in corrOption: 	
			#print corrMethod
			if(binMethod==0):
				#wlist.append(bs.binStatic(X,y,corrMethod))
				wlist.append(p.binStatic(X,y,0,corrMethod))
			elif(binMethod==1):
				#wlist.append(bs.binarySearchBins(X,y,corrMethod,0,2))
				wlist.append(p.binarySearchBins(X,y,0,corrMethod,0,2))
		weights = (ut.sumMixedCorrelation(wlist))
	rank = ut.getOrderRank(weights)
	orank = set(rank)
	#if(debug):
	#	print "original",rank
	if(cutMethod==0):
		rank = rank[0:cuts.greatestDiff(weights)]
	elif(cutMethod==1):
		rank = rank[0:cuts.monotonicValidationCut(X,y,rank,5)]
	elif(cutMethod==2):
		#rank = rank[0:cuts.fullValidationCut(X,y,rank)]
		rank = rank[0:cuts.monotonicValidationCut(X,y,rank,20)]
	if(debug):
		print "cutted",rank
	if(minRed==1):
		#rank = removeRedundant(X,rank)
		rank = p.parallelRemoveRedundant(X,rank,0)
	if(debug):
		print "mrmr",rank
	#if(len(rank)<1):
		#print "ERROR empty rank"
	#	rank = list(orank)
		#print rank
	#print "diff",orank.difference(set(rank))
	return rank