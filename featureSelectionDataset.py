import model as ml
import featureSelection as fs
from pandas import read_csv, np
import time
import util as ut

#filepath: File path of the dataset, dataset must be in format .csv, the fist row must be the name of each feature, each column is a feature except for the last column that is the objetive (target, label, value...)
#modelType: 0 classification, 1 regression, 2 autodetect
#minRed: remove redundant features (it could drastically raise the computation time)
#The result exposed in case of classification is accurracy, in case of regression is mean square error

def evaluteDataset(filepath, modelType=2, cutMethod=1, minRed=0, comporative=True): 
	data = read_csv(filepath)
	X = np.array(data.ix[:,0:-1])
	y = np.array(data.ix[:,-1])
	if(modelType>=2 or modelType<0):
		modelType = ut.datesetType(y)
	if(comporative):
		startTime = time.time()
		acc = ml.modelJudge(X=X, y=y, modelType=modelType, testPerc=0.4, runs=3)
		endTime = time.time()
		print "original:", acc, X.shape[1], str(round(endTime-startTime,3))+"s"
	startTime = time.time()
	rank = fs.featureSelection(X=X,y=y, modelType=modelType, runs=3, processes=0, corrOption=1, binMethod=0, cutMethod=cutMethod, minRed=minRed, debug=False)							
	endTime = time.time()
	timefs = round(endTime-startTime,3)
	X = np.array(data.ix[:,rank])
	startTime = time.time()
	acc = ml.modelJudge(X=X, y=y, modelType=modelType, testPerc=0.4, runs=3)
	endTime = time.time()
	timecf = round(endTime-startTime,3)
	print "result:",acc, str(timefs)+"s", str(timecf)+"s", len(rank), rank

#configuration=0   : The Fastest but could be inaccurrate
#configuration=1   : Fast and quite acurrate, without remove redundant feature (default)
#configuration=1.5 : like configuration 1 but this remove redundant features (remove redundant could be slow)
#configuration=2   : Accurrate could be slow (not recommended for dataset with a lot of features) without remove redundant
#configuration=2.5 : like configuration 2 but this remove redundant features (In most case the most accurrate and the slowest)
#comparative : when set True, shows the original dataset evaluated with our ml judges

def fcEvaluateDataset(filepath, configuration=1, comporative=True):
	if(configuration==0):
		evaluteDataset(filepath,cutMethod=0,minRed=0,comporative=comporative)
	elif(configuration==1):
		evaluteDataset(filepath,cutMethod=1,minRed=0,comporative=comporative)
	elif(configuration==1.5):
		evaluteDataset(filepath,cutMethod=1,minRed=1,comporative=comporative)
	elif(configuration==2):
		evaluteDataset(filepath,cutMethod=3,minRed=0,comporative=comporative)
	elif(configuration==2.5):
		evaluteDataset(filepath,cutMethod=3,minRed=1,comporative=comporative)

if __name__ == '__main__':
	path = 'Data/real/splice_scale.csv'
	#path = 'Data/regression/reg1000-f1.csv'
	#path = 'Data/regression/forestfires.csv'	
	fcEvaluateDataset(path)
	fcEvaluateDataset(path,configuration=1.5,comporative=False)
	fcEvaluateDataset(path,configuration=2,comporative=False)
	fcEvaluateDataset(path,configuration=2.5,comporative=False)