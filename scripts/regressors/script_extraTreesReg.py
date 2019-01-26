import sys, json
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_regression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import mutual_info_regression
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

# feature selection
# select = SelectKBest(f_regression, k=3).fit(features_train, labels_train)
# ranking = select
# cols = select.get_support(indices=True)
# rank = select.scores_
# mask = select.get_support()
# new_features = features_train.columns[mask]
# features_train = features_train[new_features]
# features_test = features_test[new_features]

# extraTrees regression
t0 = time()
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GridSearchCV

grid_param={
        'n_estimators': [50,110],
        'max_features': [2,5],
        'min_samples_split': [15,25,35]
    }

model = ExtraTreesRegressor(n_estimators=100, n_jobs=4, min_samples_split=25,
                            min_samples_leaf=35, max_features=9)
gd_sr = GridSearchCV(estimator=model,
                     param_grid=grid_param,
                    #  scoring='neg_mean_squared_error',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train, labels_train)

modelPred = gd_sr.best_score_
modeltune = gd_sr.best_params_
trainTime = round(time()-t0, 3)

print(modelPred)
print(modeltune)
print(trainTime)
