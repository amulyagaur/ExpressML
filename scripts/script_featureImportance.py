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

from sklearn.ensemble import ExtraTreesClassifier
model = ExtraTreesClassifier()
model.fit(features_train, labels_train)
print("Bagged decision trees like Random Forest and Extra Trees can be used to estimate the importance of features.")
print(model.feature_importances_)