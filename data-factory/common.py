import csv

def transposeMatrix(mlist):
	return map(list, zip(*mlist))

def getRawData(infile):
	rawData = []
	with open(infile) as f:
		reader = csv.reader(f)
		for row in reader:
			rawData.append(row)
	return rawData

def writeCSV(rawData,filepath):
	myfile = open(filepath,'w')
	for row in rawData:
		stringRow=''
		for c in row:
			stringRow+=str(c)
		stringRow = stringRow.translate(None,"\'")
		stringRow = stringRow.translate(None,"]")
		stringRow = stringRow.translate(None,"[")
		stringRow = stringRow.translate(None," ")
		myfile.write(stringRow+"\n")
	myfile.close()	

def transposeDataFile(inFile,outFile):
	data = getRawData(inFile)
	data = transposeMatrix(data)
	write = []
	for row in data:
		line = ', '.join([str(x) for x in row])
		write.append(line)
	writeCSV(write,outFile)