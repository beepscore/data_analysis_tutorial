#!/usr/bin/env python3

# Tutorial 7 Pickling
# https://pythonprogramming.net/pickle-data-analysis-python-pandas-tutorial/

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import quandl
import pickle

style.use('fivethirtyeight')

# For security keep quandl api key out of version control.
# read api key from a file that is ignored.
input_directory = "../data/input/"
input_file_name = 'quandl_api_key.txt'
input_file_path = input_directory + input_file_name
# rstrip to remove trailing \n
quandl_api_key = open(input_file_path, 'r').read().rstrip()


def us_states50():
    """
    :return: pandas series of 50 US states as 2 letter abbreviations e.g. ['AK', 'AL'...]
    """
    # https://pythonprogramming.net/dataset-data-analysis-python-pandas-tutorial
    # us_states_list is a list of dataframes
    us_states_list = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states', flavor='html5lib')

    # first dataframe
    us_states_df = us_states_list[0]

    abbreviation_series = us_states_df[0]
    # print('abbreviation_series')
    # print(abbreviation_series)

    # slice row 1 to end (omit row0, contains series name 'Abbreviation')
    # http://pandas.pydata.org/pandas-docs/stable/indexing.html#slicing-ranges
    abbreviations = abbreviation_series[1:]
    # print('abbreviations')
    # print(abbreviations)

    # python can iterate over a pandas series
    # the series contains index and value, loop uses the value
    return abbreviations


def us_states_short():
    """ 
    :return: short list of US states as 2 letter abbreviations e.g. ['ID', 'OR', 'WA']
    to avoid quandl api speed limit when looping requests
    """
    return ['ID', 'MN', 'OR', 'WA']


def grab_initial_state_data():
    """ 
    serializes pandas dataframe object and writes to file states.pickle
    text data can be saved to one of several text formats e.g. csv, json
    However can't easily save a python object such as a trained machine learning classifier to a text file.
    Instead, can serialize to a pickle.
    python has standard methods dump and load
    Alternatively, can use pandas methods to_pickle and read_pickle
    """""

    # use local variable to avoid calling function every loop iteration
    states = us_states_short()

    main_df = pd.DataFrame()

    for abbreviation in states:

        query = "FMAC/HPI_" + str(abbreviation)

        # You have exceeded the API speed limit of 20 calls per 10 minutes. Please slow down your requests.
        # http://help.quandl.com/article/68-is-there-a-rate-limit-or-speed-limit-for-api-usage
        # df = quandl.get(query)
        # use authtoken to attempt to avoid speed limit
        df = quandl.get(query, authtoken=quandl_api_key)

        # rename column 'Value' to abbreviation to avoid
        # ValueError: columns overlap but no suffix specified: Index(['Value'], dtype='object')
        df.rename(columns={'Value': str(abbreviation)}, inplace=True)

        # change state column values to percent change relative to row 0
        # don't use pct_change(), it shows change from one point to next
        df[abbreviation] = ((df[abbreviation] - df[abbreviation][0]) / df[abbreviation][0]) * 100

        if main_df.empty:
            main_df = df

        else:
            main_df = main_df.join(df)

    print('main_df')
    print(main_df)

    # original state column values
    #                    OR          WA
    # Date
    # 1975-01-31   19.688651   17.478975
    # 1975-02-28   20.174137   17.544439
    # 1975-03-31   20.634533   17.652704
    # ...
    # 2017-06-30  213.900185  216.341550
    # [510 rows x 2 columns]

    # state columns show percent change
    #                     ID          MN          OR           WA
    # Date
    # 1975-01-31    0.000000    0.000000    0.000000     0.000000
    # 1975-02-28   -0.156229    1.000795    2.465818     0.374531
    # 1975-03-31   -0.324616    1.863569    4.804198     0.993931
    # ...
    # 2017-06-30  470.938021  497.672327  986.413619  1137.724456

    # wb write bytes
    pickle_out = open('../data/output/states_change.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

###
# Tutorial 8 Percent Change and Correlation Tables
# https://pythonprogramming.net/percent-change-correlation-data-analysis-python-pandas-tutorial/


def hpi_benchmark():
    """
    """
    df = quandl.get("FMAC/HPI_USA", authtoken=quandl_api_key)
    print(df)
    us = 'United_States'

    # rename column 'Value' to us to avoid
    # ValueError: columns overlap but no suffix specified: Index(['Value'], dtype='object')
    df.rename(columns={'Value': us}, inplace=True)

    df[us] = ((df[us] - df[us][0]) / df[us][0]) * 100
    return df


# comment out after writing states.pickle
# grab_initial_state_data()

fig = plt.figure()
ax1 = plt.subplot2grid((1, 1), (0, 0))

# read data from pickle
# use python standard method
# rb read bytes
# pickle_in = open('../data/output/states.pickle', 'rb')
# HPI_data = pickle.load(pickle_in)
# print(HPI_data)

# use pandas pickle methods, slightly shorter syntax
# HPI_data.to_pickle('pickle.pickle')
HPI_data = pd.read_pickle('../data/output/states_change.pickle')

# HPI_data.plot(ax=ax1)
# HPI_data['WA'].plot(ax=ax1, label='Monthly WA HPI')

# Tutorial 9 Resampling

# pandas time series frequency offset alias A annual
# WA1yr = HPI_data['WA'].resample('A').mean()
# print(WA1yr.head())
# Date
# 1975-12-31     3.239930
# 1976-12-31    15.619957
# 1977-12-31    37.161107
# 1978-12-31    69.099914
# 1979-12-31    96.661495

# WA1yr.plot(ax=ax1, label='Yearly WA HPI')

# benchmark = hpi_benchmark()
# k is black
# benchmark.plot(ax=ax1, color='k', linewidth=6)

# plt.legend().remove
# plt.legend(loc=4)
# plt.show()

# HPI_State_Correlation = HPI_data.corr()
# print(HPI_State_Correlation)
#           ID        MN        OR        WA
# ID  1.000000  0.969281  0.994960  0.994941
# MN  0.969281  1.000000  0.970385  0.973255
# OR  0.994960  0.970385  1.000000  0.996621
# WA  0.994941  0.973255  0.996621  1.000000
# ==> states are highly correlated with each other

# statistics
# count == number of states
# min == minimum correlation with any other state
# max == maximum correlation with any other state, == 1 for same state
# 25% 25th percentile, 75% are above this value
# print(HPI_State_Correlation.describe())
#              ID        MN        OR        WA
# count  4.000000  4.000000  4.000000  4.000000
# mean   0.989796  0.978231  0.990492  0.991204
# std    0.013882  0.014609  0.013567  0.012150
# min    0.969281  0.969281  0.970385  0.973255
# 25%    0.988526  0.970109  0.988817  0.989520
# 50%    0.994951  0.971820  0.995791  0.995781
# 75%    0.996220  0.979942  0.997466  0.997466
# max    1.000000  1.000000  1.000000  1.000000

# Tutorial 10 Handling Missing Data
# https://pythonprogramming.net/nan-na-missing-data-analysis-python-pandas-tutorial/

# HPI_data['WA1yr'] = HPI_data['WA'].resample('A').mean()
# print(HPI_data[['WA', 'WA1yr']].head())
# print(HPI_data[['WA', 'WA1yr']])
# HPI_data[['WA', 'WA1yr']].plot(ax=ax1)
#                      WA       WA1yr
# Date
# 1975-01-31     0.000000         NaN
# 1975-02-28     0.374531         NaN
# 1975-03-31     0.993931         NaN
# 1975-04-30     1.756513         NaN
# 1975-05-31     2.466806         NaN
# 1975-06-30     3.221538         NaN
# 1975-07-31     4.055311         NaN
# 1975-08-31     4.568414         NaN
# 1975-09-30     4.605898         NaN
# 1975-10-31     4.697562         NaN
# 1975-11-30     5.451054         NaN
# 1975-12-31     6.687600    3.239930

# plt.legend(loc=4)
# missing values NaN prevent WA1yr from plotting
# plt.show()

# strategies to handle missing data
# ignore, delete, replace

# get rows with Nan
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.isnull.html
# print(HPI_data.isnull().values.sum())

# delete rows that contain NaN
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html
# HPI_data.dropna(inplace=True)
# HPI_data[['WA', 'WA1yr']].plot(ax=ax1)
# plt.show()

# replace NaN by filling older data forward
# HPI_data.fillna(method='ffill', inplace=True)

# replace NaN by filling with a number. Machine learning can recognize these as outliers.
# HPI_data.fillna(value=-99999, inplace=True)

# HPI_data[['WA', 'WA1yr']].plot(ax=ax1)
# plt.show()

# Tutorial 11 Rolling statistics
# https://pythonprogramming.net/rolling-statistics-data-analysis-python-pandas-tutorial/
# rolling mean aka moving average

# HPI_data['WA12MA'] = pd.rolling_mean(HPI_data['WA'], 12)
# FutureWarning: pd.rolling_mean is deprecated for Series and will be removed in a future version, replace with
# Series.rolling(window=12,center=False).mean()
HPI_data['WA12MA'] = HPI_data['WA'].rolling(window=12, center=False).mean()

print(HPI_data[['WA', 'WA12MA']].head())
HPI_data[['WA', 'WA12MA']].plot(ax=ax1)

plt.legend(loc=4)
plt.show()
