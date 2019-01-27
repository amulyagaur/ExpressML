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

modelPred = []
trainTime = []
modeltune = []
id=0



# extraTrees regression
t0 = time()
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GridSearchCV

grid_param={
        'n_estimators': [50,110],
        'min_samples_split': [15,25,35]
    }

model = ExtraTreesRegressor(n_estimators=100, n_jobs=4, min_samples_split=25,
                            min_samples_leaf=35)
gd_sr = GridSearchCV(estimator=model,
                     param_grid=grid_param,
                    #  scoring='neg_mean_squared_error',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train, labels_train)
id=id+1
modelPred.append((gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0, 3))

#lasso regression
t0 = time()
from sklearn import linear_model
reg = linear_model.Lasso()
grid_param={'alpha': [10,4,1.0,0.5,0.3,0.08,0.02]}

from sklearn.model_selection import GridSearchCV

gd_sr = GridSearchCV(estimator=reg,
                     param_grid=grid_param,
                    #  scoring='neg_mean_squared_error',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train, labels_train)
id=id+1
modelPred.append((gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0, 3))


# ridge regression
t0 = time()
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

grid_param={'alpha': [10,4,1.0,0.5,0.3,0.08,0.02]}
rdg_reg = Ridge()
gd_sr = GridSearchCV(estimator=rdg_reg,
                     param_grid=grid_param,
                    #  scoring='neg_mean_squared_error',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train, labels_train)
id=id+1
modelPred.append((gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0, 3))

# linear regression
t0 = time()
from sklearn.linear_model import LinearRegression
grid_param = {'fit_intercept': [True, False], 
    'normalize': [True, False], 
    'copy_X': [True, False]
}
reg = LinearRegression()
gd_sr = GridSearchCV(estimator=reg,
                     param_grid=grid_param,
                    #  scoring='neg_mean_squared_error',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train, labels_train)
id=id+1
modelPred.append((gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0, 3))


print (modelPred)
print (modeltune)
print (trainTime)