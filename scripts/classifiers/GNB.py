import sys, json
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from time import time 

lines = sys.stdin.readlines()
trainfeatures = lines[0][1:-2]
label =lines[1][:-1]
filename = lines[2][:-1]

df = pd.read_csv(filename) 	

train,test = train_test_split(df,test_size=0.9)

features='\",'+trainfeatures+',\"'
feat = features.split('","')
feat = feat[1:-1]
desiredno = len(feat)

features_test = test[feat]

labels_train = train[label]

features_train = train[feat]

labels_test = test[label]
#feature selection
select = SelectKBest(chi2, k="all").fit(features_train, labels_train)
ranking = select
cols = select.get_support(indices=True)
rank = select.scores_
mask = select.get_support()
new_features = features_train.columns[mask]
features_train = features_train[new_features]
features_test = features_test[new_features]

# Gaussian naive_bayes :
t0 = time()
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(features_train, labels_train)
modelPred = 100*clf.score(features_test,labels_test)
trainTime = (time()-t0)
print(modelPred)
print(trainTime) 
