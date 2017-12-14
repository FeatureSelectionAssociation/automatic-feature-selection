def greatestDiff(lst):
	maxdiff=0
	cutpos=0
	for i in range(0,len(lst)-1):
		diff = lst[i]-lst[i+1]
		if(diff>maxdiff):
			maxdiff = diff
			cutpos = i+1
	return cutpos

