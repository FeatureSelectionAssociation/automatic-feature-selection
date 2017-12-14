import common as cm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

testPerc = 0.5
data = cm.readNumpy("datasets/data.csv",'label')
[X,y,headers] = data
X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=testPerc, random_state=43)

#pca = PCA(n_components=3)
#X_r = pca.fit(X).transform(X)

lda = LinearDiscriminantAnalysis(n_components=3)
X_r2 = lda.fit(X_train, y_train).transform(X)

print X_r2 