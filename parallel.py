import time
import multiprocessing

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
	return indexes

def tuplesPoolGenerator(size,nsplits):
	sArray = splitArray(size,nsplits)
	tl = []
	for i in range(0,len(sArray)-1):
		tl.append([sArray[i],sArray[i+1]])
	return tuple(tl)

def splitInformation(info,nsplits):
	tl = tuplesPoolGenerator(len(info),nsplits)
	sInfo = []
	for i in tl:
		sInfo.append( info[i[0]:i[1]])
	return sInfo

