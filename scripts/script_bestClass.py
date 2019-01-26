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
featno = lines[3][:-1]
feat_no = int(featno)

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
id=1



# print "KNN :"
t0 =time()
grid_param = {'n_neighbors':[1,2,3],
          'leaf_size':[2,5],
          'weights':['uniform', 'distance'],
          'algorithm':['auto', 'ball_tree','kd_tree','brute'],
          'n_jobs':[-1]}
from sklearn.neighbors import KNeighborsClassifier
clf1 = KNeighborsClassifier(n_neighbors=3,algorithm='ball_tree')
gd_sr = GridSearchCV(estimator=clf1,  
                     param_grid=grid_param,
                     scoring='accuracy',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train,labels_train)
id=id+1
modelPred.append((100*gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0,3))

# Logistic Regression: 
t0 =time()
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
grid={"C":np.logspace(-3,3,7), "penalty":["l1","l2"]}# l1 lasso l2 ridge
logreg=LogisticRegression()
gd_sr = GridSearchCV(estimator=logreg,  
                     param_grid=grid,
                     scoring='accuracy',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train,labels_train)
id=id+1
modelPred.append((100*gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0,3))


# print "SVM :"
t0 =time()
grid_param = {'C': [6,10,12], 
          'kernel': ['linear','rbf']}
from sklearn.svm import SVC
clf3 = SVC()
clf3.fit(features_train,labels_train)
gd_sr = GridSearchCV(estimator=clf3,  
                     param_grid=grid_param,
                     scoring='accuracy',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train,labels_train)
id=id+1
modelPred.append((100*gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0,3))

# print "Random Forest: "
t0 =time()
grid_param = {  
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy'],
    'bootstrap': [True, False]
}
from sklearn.ensemble import RandomForestClassifier
clf4 = RandomForestClassifier(max_depth=2, random_state=0)
gd_sr = GridSearchCV(estimator=clf4,  
                     param_grid=grid_param,
                     scoring='accuracy',
                     cv=2,
                     n_jobs=-1)
gd_sr.fit(features_train,labels_train)
id=id+1
modelPred.append((100*gd_sr.best_score_,id))
modeltune.append(gd_sr.best_params_)
trainTime.append(round(time()-t0,3))

# print "Gaussian naive_bayes :"
t0 = time()
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(features_train, labels_train)
modelPred.append((100*clf.score(features_test,labels_test),id))
trainTime.append(time()-t0)

print (modelPred)
print (modeltune)
print (trainTime)