# Tutorial 15 Rolling Apply and Mapping Functions
# https://pythonprogramming.net/rolling-apply-mapping-functions-data-analysis-python-pandas-tutorial/
# tutorial author said he uses map function frequently, almost never uses rolling_apply

import pandas as pd
from matplotlib import style
import numpy as np
from sklearn import svm, preprocessing, model_selection

from statistics import mean
style.use('fivethirtyeight')

# For security keep quandl api key out of version control.
# read api key from a file that is ignored.
input_directory = "../data/input/"
input_file_name = 'quandl_api_key.txt'
input_file_path = input_directory + input_file_name
# rstrip to remove trailing \n
quandl_api_key = open(input_file_path, 'r').read().rstrip()


# read data from tutorial 14 pickle, use pandas method
housing_data = pd.read_pickle('../data/output/hpi_extended.pickle')

# percent change relative to previous row, not relative to row 0
# Note I already did dropna before pickling.
housing_data = housing_data.pct_change()

# pct_change generates values like +/- infinity in row 0. Replace them with NaN.
housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)

# shift up one row
housing_data['US_HPI_future'] = housing_data['United_States'].shift(-1)

housing_data.dropna(inplace=True)


def get_label(cur_hpi, fut_hpi):
    """ return a label that can be used as input to a machine learning classifier.
    supervised machine learning uses features and label.
    """
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0


def moving_average(values):
    """pandas has a moving average function,
    implement our own to call in an example for rolling apply
    """
    return mean(values)


# map function get_label over input feature lists to column 'label'
# features are independent variables like gdp, unemp_rate
housing_data['label'] = list(map(get_label, housing_data['United_States'], housing_data['US_HPI_future']))

# print(housing_data.head())
#             United_States       m30  unemp_rate       gdp     sp500  \
# Date
# 1990-03-31       0.004474  0.090909    0.090909 -0.234375  0.031580
# 1990-04-30       0.005365  0.119048   -0.166667  4.265306 -0.034758
# 1990-05-31       0.005286  0.117021    0.000000 -1.092539  0.119888
# 1990-06-30       0.005138 -0.304762    0.200000  3.115183 -0.011293
# 1990-07-31       0.003759 -0.164384   -0.250000  0.441476 -0.006654
#
#             US_HPI_future  label
# Date
# 1990-03-31       0.005365      1
# 1990-04-30       0.005286      0
# 1990-05-31       0.005138      0
# 1990-06-30       0.003759      0
# 1990-07-31       0.000536      0

# housing_data['ma_apply_example'] = housing_data['m30'].rolling(window=10, center=False).apply(func=moving_average)
# print(housing_data.tail())
#             United_States       m30  unemp_rate       gdp     sp500  \
# Date
# 2013-11-30      -0.002459 -0.013359   -0.250000 -0.030867  0.029335
# 2013-12-31      -0.002382 -0.038685   -0.500000 -0.013613  0.024612
# 2014-01-31       0.000747  0.006036   -0.333333 -0.045316 -0.037129
# 2014-02-28       0.006798  0.026000    0.500000  0.008535  0.045063
# 2014-03-31       0.012600 -0.007797    0.000000  0.048984  0.007232
#
#             US_HPI_future  label  ma_apply_example
# Date
# 2013-11-30      -0.002382      1         -0.014369
# 2013-12-31       0.000747      1         -0.016244
# 2014-01-31       0.006798      1         -0.014963
# 2014-02-28       0.012600      1         -0.014410
# 2014-03-31       0.014471      1         -0.013685

# Tutorial 16 Scikit Learn
# https://pythonprogramming.net/scikit-learn-sklearn-machine-learning-data-analysis-python-pandas-tutorial/
# Choosing the right estimator
# http://scikit-learn.org/stable/tutorial/machine_learning_map/index.html
# by convention, features uppercase X, label lowercase y.

# http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.drop.html
# housing_data_dropped = housing_data.drop(['label', 'US_HPI_future'], 1)
# explicitly show parameter names
housing_data_dropped = housing_data.drop(labels=['label', 'US_HPI_future'], axis=1)

# convert to numpy array
X = np.array(housing_data_dropped)
# print(X)
# [[  4.47422978e-03   9.09090909e-02   9.09090909e-02  -2.34375000e-01 3.15797208e-02]
#  [  5.36539969e-03   1.19047619e-01  -1.66666667e-01   4.26530612e+00 -3.47581915e-02]
#  [  5.28599268e-03   1.17021277e-01   0.00000000e+00  -1.09253876e+00 1.19888207e-01]
#  ...,
#  [  7.46858348e-04   6.03621730e-03  -3.33333333e-01  -4.53164647e-02 -3.71292550e-02]
#  [  6.79786610e-03   2.60000000e-02   5.00000000e-01   8.53517014e-03 4.50630488e-02]
#  [  1.26001924e-02  -7.79727096e-03   0.00000000e+00   4.89835814e-02 7.23154688e-03]]

# scale -1 to +1
# X = preprocessing.scale(X)
# print(X)
# [[ 0.14408056  0.23373543  0.27207146 -0.39346702  0.51027382]
#  [ 0.25286537  0.31922935 -0.58269194  4.49674873 -0.90138653]
#  [ 0.24317219  0.31307267 -0.02960974 -1.3261122   2.38946453]
#  ...,
#  [-0.31091841 -0.02413573 -1.13577414 -0.18799979 -0.95184238]
#  [ 0.42772607  0.03652068  1.62963686 -0.12947428  0.79719692]
#  [ 1.13601409 -0.06616633 -0.02960974 -0.08551529 -0.0078515 ]]

# y 'label' will be the classification
y = np.array(housing_data['label'])

# test size 20% of the data, train on 80%
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# classifier support vector machine / support vector classification
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

# print(clf.score(X_test, y_test))
# 0.51724137931
# not very good!
# tutorial got 0.74
# tutorial X indludes 55 columns, hpi for US and for every state
# housing_data has ~ 5 columns, hpi for us but not for any state.

