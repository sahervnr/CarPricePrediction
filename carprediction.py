# -*- coding: utf-8 -*-
"""Carprediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nCKHv5j0EfsPFbznQP7m9OVgb6Tf0HdK
"""

from google.colab import files
fil=files.upload()

import pandas as pd

df=pd.read_csv('car data.csv')

df.head()

df.shape

print(df['Seller_Type'].unique())
print(df['Transmission'].unique())
print(df['Owner'].unique())

df.isnull().sum()

df.describe()

df.columns

final_dataset=df[['Year', 'Selling_Price', 'Present_Price', 'Kms_Driven',
       'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']]

final_dataset.head()

final_dataset['Current_Year']=2021

final_dataset.head()

final_dataset['no_year']=final_dataset['Current_Year']-final_dataset['Year']

final_dataset.head()

final_dataset.drop(['Year','Current_Year'],axis=1,inplace=True)

final_dataset.head()

final_dataset=pd.get_dummies(final_dataset,drop_first=True)

final_dataset.head()

final_dataset.corr()

import seaborn as sns

sns.pairplot(final_dataset)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline
corrmat=final_dataset.corr()
top_corr_features=corrmat.index
plt.figure(figsize=(20,20))
g=sns.heatmap(final_dataset[top_corr_features].corr(),annot=True,cmap="RdYlGn")

final_dataset.head()

X=final_dataset.iloc[:,1:]
y=final_dataset.iloc[:,0]

X.head()

y.head()

from sklearn.ensemble import ExtraTreesRegressor
model=ExtraTreesRegressor()
model.fit(X,y)

print(model.feature_importances_)

feat_importances=pd.Series(model.feature_importances_,index=X.columns)
feat_importances.nlargest(5).plot(kind='barh')
plt.show()

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

X_train.shape

from sklearn.ensemble import RandomForestRegressor
rf_random=RandomForestRegressor()

import numpy as np
n_estimators=[int(x) for x in np.linspace(start=100,stop=1200,num=12)]
max_features=['auto','sqrt']
max_depth=[int(x) for x in np.linspace(5,30,num=6)]
min_samples_split=[2,5,10,15,100]
min_samples_leaf=[1,2,5,10]

from sklearn.model_selection import RandomizedSearchCV

random_grid={'n_estimators':n_estimators,'max_features':max_features,'max_depth':max_depth,'min_samples_split':min_samples_split,'min_samples_leaf':min_samples_leaf}
print(random_grid)

rf=RandomForestRegressor()

rf_random=RandomizedSearchCV(estimator=rf,param_distributions=random_grid,scoring='neg_mean_squared_error',n_iter=10,cv=5,verbose=2,random_state=42,n_jobs=1)

rf_random.fit(X_train,y_train)

predictions=rf_random.predict(X_test)

predictions

sns.distplot(y_test-predictions)

plt.scatter(y_test,predictions)

import pickle
file=open('random_forest_regression_model.pkl','wb')
pickle.dump(rf_random,file)

!pip freeze>requirements.txt

