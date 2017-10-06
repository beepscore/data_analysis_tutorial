# Tutorial 15 Rolling Apply and Mapping Functions
# https://pythonprogramming.net/rolling-apply-mapping-functions-data-analysis-python-pandas-tutorial/
# tutorial author said he uses map function frequently, almost never uses rolling_apply

import pandas as pd
from matplotlib import style
import numpy as np
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


def create_labels(cur_hpi, fut_hpi):
    """ predict.
    will feed into machine learning classifier.
    supervised machine learning has features and label.
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


# use map to generate the label
# map function create_labels from input features to column 'label'
# features are independent variables like gdp, unemp_rate
housing_data['label'] = list(map(create_labels, housing_data['United_States'], housing_data['US_HPI_future']))

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

# TODO: fix warning
# FutureWarning: pd.rolling_apply is deprecated for Series and will be removed in a future version, replace with
# Series.rolling(window=10,center=False).apply(func=<function>,args=<tuple>,kwargs=<dict>)
#  housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['m30'], 10, moving_average)
housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['m30'], 10, moving_average)
print(housing_data.tail())
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
