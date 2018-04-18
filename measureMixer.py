def sumMixedCorrelation(ll):
	arr = [sum(x) for x in zip(*ll)]
	maxValue = max(arr)
	return [round(x / maxValue,2) for x in arr]