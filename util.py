import copy


def findInList(mlist, mvar):
	for i in range(0,len(mlist)):
		if(mlist[i]==mvar):	return i
	return False

def removeColumnFromList(mlist,column):
	return [c.pop(column) for c in mlist]
	
def copyList(mlist):
	return mlist

def removeColumnByName(data,label,removeHeader=1):
	indexLabel = findInList(data[0],label)
	if(removeHeader): data.pop(0)
	return removeColumnFromList(data,indexLabel)

def transposeMatrix(mlist):
	return map(list, zip(*mlist))
