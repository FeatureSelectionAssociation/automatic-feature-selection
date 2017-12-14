import featureSelector as fs
import classifiers as cf
from pandas import *


def artificialTest():
	#xbinset = [2, 4, 7, 10, 15, 20, 30, 40, 50, 75, 100, 200] #features
	xbinset = [2, 4, 7, 10, 15, 20, 30, 40, 50, 75, 100] #features
	ybinset = [2] #label
	files = ['flex-ct-train.csv', 'data-f1.csv', 'data-f2.csv','data-f3.csv','data-f4.csv']
	buenos = [[0],[1,2,3,4,5,6],[0,1],[0,1],[0,1,3,2]]
	#files = ['data-f1.csv']
	i = 0

	for f in files:
		filename = 'Data/'+f
		print filename, buenos[i]
		data = read_csv(filename)
		print "static"
		fs.get_bestcorlab(xbinset, ybinset, data)
		print "dynamic"
		X = np.array(data.ix[:,0:-1])
		y = np.array(data.ix[:,-1])
		cf.getBestClassifiers(X,y)
		[X,y] = fs.get_bestcorlabDynamic(data)
		cf.getBestClassifiers(X,y)
		i = i+1
		print("\n")
artificialTest()


#print "Data\data2400-r20" #buenos 0,1,2 #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data2400-r20.csv', 24, 23)
#print "Data\data-f1" # 1,2,3,4,5,6 #Observaciones: Corte complicado por la distancia
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f1.csv', 14, 13)
#print "Data\data-f2" #0,1  #Observaciones: EXCELENTE (mas bins)
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f2.csv', 9, 8)
#print "Data\data-f2-fe" #0,1  #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f2-fe.csv', 11, 10)
#print "Data\data-f3" #0,1 Observaciones: Corte complicado, debido a que una de las 2 caracteristicas esta muy bien evaluada y la otra esta muy cerca del ruido
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f3.csv', 7, 6)
#print "Data\data-f4" #0,1,2,3 #Observaciones: Excelente
#fs.get_bestcorlabNoComb(xbinset, ybinset, 'Data\data-f4.csv', 7, 6)

#print "Data/data-regression.csv" #0,1,2,3 #Observaciones: Excelente
#fs.get_bestcorlab(xbinset, ybinset, 'Data/data-regression.csv', 37, 36)
