"""
Testing various models on the change dataset
"""

#import dependencies
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras import backend as K
from sklearn.metrics import mean_absolute_error
import catboost as cb
from sklearn.multioutput import MultiOutputRegressor

#import dataset
synth_df = pd.read_csv("datasets/synth_gad-phq.csv", index_col=0)

#get dummy variables
dummies = pd.get_dummies(synth_df.iloc[:, 18])


#split to x and y, adding in dummy variables
X = synth_df.iloc[:, :18]
X = X.join(dummies)
y = synth_df.iloc[:, 19:]

#split training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

#create a multioutput catboost regressor, train it and predict
model = MultiOutputRegressor(cb.CatBoostRegressor())
model.fit(X_train, y_train)
yhat = model.predict(X_test)

#assess
print("RMSE: ",round(np.sqrt(np.mean((yhat - y_test)**2, axis=0)), 3))
print("MSE: ",round(np.mean((yhat - y_test)**2, axis=0), 3))
print("MAE: ",round(mean_absolute_error(y_test, yhat), 3))
