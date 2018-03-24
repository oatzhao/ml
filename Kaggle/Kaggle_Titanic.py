#-*- coding:utf-8 -*-
#!/usr/bin/python

import pandas
import numpy as np

#读文件
titanic = pandas.read_csv('/Users/zhaoyan20/PycharmProjects/ML/Kaggle/datas/train.csv')
#print titanic.describe()
print titanic.head()
titanic['Age'] = titanic['Age'].fillna(titanic['Age'].median())#对缺失值用平均值填充
#print titanic.describe()
print titanic['Sex'].unique()
titanic.loc[titanic['Sex'] == 'male','Sex'] = 0 #loc定位到哪一行，将titanic['Sex'] == 'male'的样本Sex值改为0
titanic.loc[titanic['Sex'] == 'female','Sex'] = 1
print titanic['Sex'].unique()
print titanic['Embarked'].unique()
titanic['Embarked'] = titanic['Embarked'].fillna('S')     #用最多的填
titanic.loc[titanic['Embarked'] == 'S','Embarked'] = 0
titanic.loc[titanic['Embarked'] == 'C','Embarked'] = 1
titanic.loc[titanic['Embarked'] == 'Q','Embarked'] = 2
print titanic['Embarked'].unique()
from sklearn.linear_model import LinearRegression #线性回归
from sklearn.cross_validation import KFold #交叉验证库，将测试集进行切分交叉验证取平均
predictors = ['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']   #用到的特征
alg = LinearRegression()
kf = KFold(titanic.shape[0],n_folds=3,random_state=1) #将m个样本平均分成3份进行交叉验证

predictions = []
for train, test in kf:
    print train
    print test
    train_predictors = (titanic[predictors].iloc[train, :])  # 将predictors作为测试特征
    train_target = titanic['Survived'].iloc[train]
    alg.fit(train_predictors, train_target)
    test_prediction = alg.predict(titanic[predictors].iloc[test, :])
    print len(test_prediction)
    predictions.append(test_prediction)

predictions = np.concatenate(predictions, axis= 0)
print len(predictions)
predictions[predictions > .5] = 1
predictions[predictions <= .5] = 0
print predictions
accury = sum(predictions[predictions == titanic['Survived']]) / len(predictions)#测试准确率
print accury

from sklearn.linear_model import LogisticRegression #逻辑回归
from sklearn import cross_validation
alg = LogisticRegression(random_state=1)
scores = cross_validation.cross_val_score(alg, titanic[predictors],titanic['Survived'],cv=3)
print scores.mean()


from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
predictions = ['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']
alg = RandomForestClassifier(random_state=1,n_estimators=50,min_samples_split=4,min_samples_leaf=2)
kf = cross_validation.KFold(titanic.shape[0],n_folds=3,random_state=1)
scores = cross_validation.cross_val_score(alg,titanic[predictors],titanic['Survived'],cv=kf)
print scores.mean()

titanic['Familysize'] = titanic['SibSp'] + titanic['Parch']
titanic['NameLength'] = titanic['Name'].apply(lambda  x:len(x))

import re
def get_title(name):
    title_reserch = re.search('([A-Za-z]+)\.', name)
    if title_reserch :
        return title_reserch.group(1)
    return ""
titles = titanic['Name'].apply(get_title)
print pandas.value_counts(titles)
title_mapping = {"Mr":1,"Miss":2,"Mrs":3,"Master":4,"Dr":5,"Rev":6,"Col":7,"Major":8,"Mlle":9,"Countess":10,"Ms":11,"Lady":12,"Jonkheer":13,"Don":14,"Mme":15,"Capt":16,"Sir":17}

for k,v in title_mapping.items():
    print '****',k,v
    titles[titles == k] = v
print (pandas.value_counts(titles))
titanic["titles"] = titles #添加title特征



import numpy as np
from sklearn.feature_selection import SelectKBest,f_classif#引入feature_selection看每一个特征的重要程度
import matplotlib.pyplot as plt

predictors = ['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Familysize','NameLength','titles']
selector = SelectKBest(f_classif,k=5)
selector.fit(titanic[predictors],titanic['Survived'])
print selector.pvalues_
scores = -np.log10(selector.pvalues_)
print scores
plt.bar(range(len(predictors)),scores)
plt.xticks(range(len(predictors)),predictors,rotation='vertical')
plt.show

from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
algorithas = [
        [GradientBoostingClassifier(random_state=1,n_estimators=25,max_depth=3),['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Familysize','NameLength','titles']],
        [LogisticRegression(random_state=1),['Pclass','Sex','Age','SibSp','Parch','Fare','Embarked','Familysize','NameLength','titles']]
        ]
kf = KFold(titanic.shape[0],n_folds=3,random_state=1)
predictions = []
for train, test in kf:
   train_target = titanic['Survived'].iloc[train]
   full_test_predictions = []
   for alg,predictors in algorithas:
       alg.fit(titanic[predictors].iloc[train,:],train_target)
       test_prediction = alg.predict_proba(titanic[predictors].iloc[test,:].astype(float))[:,1]
       full_test_predictions.append(test_prediction)
   test_predictions = (full_test_predictions[0] + full_test_predictions[1]) / 2
   test_predictions[test_predictions >.5] = 1
   test_predictions[test_predictions <=.5] = 0
   predictions.append(test_predictions)
predictions = np.concatenate(predictions,axis=0)
accury = sum(predictions[predictions == titanic['Survived']]) / len(predictions)#测试准确率
print accury
