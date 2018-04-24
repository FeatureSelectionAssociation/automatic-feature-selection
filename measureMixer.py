#from operator import add

def sumMixedCorrelation(ll, normalize=False):
	ll = normalizeScales(ll)
	arr = [round(sum(x)/len(ll),2) for x in zip(*ll)]
	if(normalize):
		maxValue = max(arr)
		return [round(x / maxValue,2) for x in arr]
	else:
		return arr

def findMultiplier(ll):
	w = [max(sublist) for sublist in ll]
	w = [max(w)]*len(w)
	#print w
	i = 0
	for l in ll:
		w[i] = round(float(w[i])/max(l),2)
		i = i+1
	return w

def normalizeScales(ll):
	w = findMultiplier(ll)
	#print w
	for i in range(len(ll)):
		for j in range(len(ll[i])):
			ll[i][j] = round(ll[i][j]*w[i],2)
	return ll



