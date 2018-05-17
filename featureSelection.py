import util as ut
import binSelection as bs
import cuts
from pandas import read_csv, np
import CorrelationMesures as cm

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
def featureSelection(X,y, corrOption=4, binMethod=0, cutMethod=1, minRed=True, debug=True):
	if(corrOption<=3):
		corrMethod = corrOption
	elif(corrOption==4):
		corrOption = [0,1]
	elif(corrOption==5):
		corrOption = [0,1,3]
	wlist = []
	if(corrOption<=3):
		if(binMethod==0):
			weights = bs.binStatic(X,y,corrMethod)
		elif(binMethod==1):
			weights = bs.binarySearchBins(X,y,corrMethod,0,2)
	else:
		for corrMethod in corrOption: 	
			#print corrMethod
			if(binMethod==0):
				wlist.append(bs.binStatic(X,y,corrMethod))
			elif(binMethod==1):
				wlist.append(bs.binarySearchBins(X,y,corrMethod,0,2))
		weights = (ut.sumMixedCorrelation(wlist))
	rank = ut.getOrderRank(weights)
	orank = set(rank)
	#if(debug):
	#	print "original",rank
	if(cutMethod==0):
		rank = rank[0:cuts.greatestDiff(rank)]
	elif(cutMethod==1):
		rank = rank[0:cuts.monotonicValidationCut(X,y,rank)]
	elif(cutMethod==2):
		rank = rank[0:cuts.fullValidationCut(X,y,rank)]
	if(debug):
		print "cutted",rank
	if(minRed):
		rank = removeRedundant(X,rank)
	if(debug):
		print "mrmr",rank
	#if(len(rank)<1):
		#print "ERROR empty rank"
	#	rank = list(orank)
		#print rank
	#print "diff",orank.difference(set(rank))
	return rank