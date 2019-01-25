import sys, json
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from time import time 

df = pd.read_csv("data.csv") 	

train,test = train_test_split(df,test_size=0.9)

lines = sys.stdin.readlines()

trainfeatures = lines[0][1:-2]
label =lines[1][:-1]

features='\",'+trainfeatures+',\"'
feat = features.split('","')
feat = feat[1:-1]
desiredno = len(feat)

features_test = test[feat]

labels_train = train[label]

features_train = train[feat]

labels_test = test[label]

#feature selection
select = SelectKBest(chi2, k=3).fit(features_train, labels_train)
selected_cols = select.get_support(indices=True)
feature_score = select.scores_
print(feature_score)
print(selected_cols)
