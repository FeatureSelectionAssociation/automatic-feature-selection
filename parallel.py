import multiprocessing
import binSelection as bs
from functools import partial

def splitArray(number, size):
	ss = number/float(size)
	indexes = []
	current = 0
	while (current<=number):
		indexes.append(current)
		current += ss
	for i in range(0,len(indexes)):
		indexes[i] = int(indexes[i])
	if((number-1)>indexes[-1]):
		indexes.append(number)
	elif(indexes[-1]>=(number-1)):
		indexes[-1] = number
	indexes = list(set(indexes))
	indexes.sort()
	return indexes

def tuplesPoolGenerator(size,nsplits):
	sArray = splitArray(size,nsplits)
	tl = []
	for i in range(0,len(sArray)-1):
		tl.append([sArray[i],sArray[i+1]])
	return tuple(tl)

def splitInformation(info,nsplits):
	tl = tuplesPoolGenerator(int(info.shape[1]),nsplits)
	sInfo = []
	for i in tl:
		sInfo.append(info[:,i[0]:i[1]])
	return tuple(sInfo)

def binStatic(X, y, processes=0, method=2):
	cores = multiprocessing.cpu_count()
	nfeat = X.shape[1]
	#if(nfeat*pow(len(list(set(y))),0.5)*pow(cores,0.5)*len(y)*2>500000): 
	if(processes==0):
		jobs = cores
		if(cores>nfeat):
			jobs = nfeat
	else:	
		jobs=processes
	pool = multiprocessing.Pool(processes=jobs)
	info = splitInformation(X,jobs)
	pbs=partial(bs.binStatic, y=y, method=method)
	presults = pool.map(pbs, info)
	results = [item for sublist in presults for item in sublist]
	return results
	

def binarySearchBins(X, y, processes=0, method=0, split=0, useSteps=0, normalizeResult=False, debug=False):
	if(processes==0):
		nfeat = X.shape[1]
		cores = multiprocessing.cpu_count()
		jobs = cores
		if(cores>nfeat):
			jobs = nfeat
	else:	
		jobs=processes
	pool = multiprocessing.Pool(processes=jobs)
	info = splitInformation(X,jobs)
	pbs=partial(bs.binarySearchBins, y=y, method=method, split=split, useSteps=useSteps, normalizeResult=normalizeResult, debug=debug)
	presults = pool.map(pbs, info)
	results = [item for sublist in presults for item in sublist]
	return results