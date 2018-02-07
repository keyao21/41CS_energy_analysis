# Compare Algorithms
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

#sklearn stuff
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix, mean_squared_error, r2_score

from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor

#testing 
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle

#analyzing results
from sklearn import metrics
from sklearn.metrics import make_scorer
from sklearn.model_selection import learning_curve
from sklearn.metrics import r2_score, mean_squared_error

df = pd.read_csv('CU_UtilityData.csv', dtype={'Utility Subtotal':np.float64}, na_values={'Invalid', ' '})
df = df.dropna()
df = df.drop('DATE', axis=1)
df['Utility Subtotal'] = pd.to_numeric(df['Utility Subtotal'])

# df.to_csv('CU_UtilityData_ky.csv')

array = df.values
array_train = array[:math.ceil(len(array)*.8)]
X = array_train[:,0:-1]
Y = array_train[:,-1]

array_test = array[math.ceil(len(array)*.8):]
X_test = array_test[:,0:-1]
Y_test = array_test[:,-1]

# prepare configuration for cross validation test harness
seed = 7

# prepare models
model = DecisionTreeRegressor()

clf = model.fit(X, Y)
y_predict = clf.predict(X_test)
print(r2_score(y_predict, clf.predict(X_test)))
print(clf.score(X_test, y_predict))


scoring = make_scorer(r2_score)
g_cv = GridSearchCV(DecisionTreeRegressor(random_state=0),
              param_grid={'min_samples_split': range(2, 10)},
              scoring=scoring, cv=5, refit=True)

g_cv.fit(X, Y)
g_cv.best_params_

result = g_cv.cv_results_
# print(result)
r2_score(Y_test, g_cv.best_estimator_.predict(X_test))