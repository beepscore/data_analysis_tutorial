# Tutorial 15 Rolling Apply and Mapping Functions
# https://pythonprogramming.net/rolling-apply-mapping-functions-data-analysis-python-pandas-tutorial/

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

housing_data = housing_data.pct_change()

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)

# shift up one row
housing_data['US_HPI_future'] = housing_data['United_States'].shift(-1)

# I think I already did dropna before pickling, tutorial shows to do it now.
housing_data.dropna(inplace=True)

# supervised machine learning has features and label
# features are independent variables like gdp, unemp_rate
# generate the label fut_hpi

def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

housing_data['label'] = list(map(create_labels, housing_data['United_States'], housing_data['US_HPI_future']))
print(housing_data.head())
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


