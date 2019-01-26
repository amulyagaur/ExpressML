from sklearn import linear_model
import sys
import json
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from time import time

df = pd.read_csv("data.csv")

train, test = train_test_split(df, test_size=0.9)

lines = sys.stdin.readlines()

trainfeatures = lines[0][1:-2]
label = lines[1][:-1]

features = '\",'+trainfeatures+',\"'
feat = features.split('","')
feat = feat[1:-1]
desiredno = len(feat)

features_test = test[feat]

labels_train = train[label]

features_train = train[feat]

labels_test = test[label]

# feature selection
select = SelectKBest(chi2, k=3).fit(features_train, labels_train)
ranking = select
cols = select.get_support(indices=True)
rank = select.scores_
mask = select.get_support()
new_features = features_train.columns[mask]
features_train = features_train[new_features]
features_test = features_test[new_features]

# linear regression
t0 = time()
grid_param = {'fit_intercept': [True, False], 'normalize': [
    True, False], 'copy_X': [True, False]}
reg = linear_model.LinearRegression()
gd_sr = GridSearchCV(estimator=reg,
                     param_grid=grid_param,
                     scoring='accuracy',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train, labels_train)

modelPred = 100*gd_sr.best_score_
modeltune = gd_sr.best_params_
trainTime = round(time()-t0, 3)

print(modelPred)
print(modeltune)
print(trainTime)
