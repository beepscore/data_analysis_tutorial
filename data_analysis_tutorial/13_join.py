
# Tutorial 13
# https://pythonprogramming.net/joining-mortgage-rate-data-analysis-python-pandas-tutorial/
# based on house_prices.py

import quandl
import pandas as pd
import pickle
from matplotlib import style

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
    us = 'United_States'

    # rename column 'Value' to us to avoid
    # ValueError: columns overlap but no suffix specified: Index(['Value'], dtype='object')
    df.rename(columns={'Value': us}, inplace=True)

    df[us] = ((df[us] - df[us][0]) / df[us][0]) * 100
    return df


def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=quandl_api_key)
    df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0

    # fix warning
    # .resample() is now a deferred operation You called resample(...) on this deferred object
    # which materialized it into a dataframe by implicitly taking the mean.\
    # Use.resample(...).mean() instead
    df = df.resample('1D').mean()
    df = df.resample('M').mean()
    return df


# comment out after writing states.pickle
# grab_initial_state_data()

# read data from pickle
# use python standard method
# rb read bytes
pickle_in = open('../data/output/states.pickle', 'rb')
HPI_data = pickle.load(pickle_in)
# print()
# print('HPI_data')
# print(HPI_data)

# use pandas pickle methods, slightly shorter syntax
# HPI_data.to_pickle('pickle.pickle')
# HPI_data = pd.read_pickle('../data/output/states_change.pickle')

HPI_Bench = hpi_benchmark()
print()
print('HPI_Bench head')
print(HPI_Bench.head())
#             United_States
# Date
# 1975-01-31       0.000000
# 1975-02-28       0.657772
# 1975-03-31       1.722313
# 1975-04-30       3.106105
# 1975-05-31       3.974628

print()
m30 = mortgage_30y()
m30.columns = ['M30']
print('m30')
print(m30)
# m30
#                   M30
# Date
# 1975-01-31   0.000000
# 1975-02-28  -3.393425
# 1975-03-31  -5.620361
# 1975-04-30  -6.468717
# 1975-05-31  -5.514316
# ...
# 2016-09-30 -63.308590

HPI = HPI_Bench.join(m30)
print()
print('join')
print(HPI.head())
#             United_States       M30
# Date
# 1975-01-31       0.000000  0.000000
# 1975-02-28       0.657772 -3.393425
# 1975-03-31       1.722313 -5.620361
# 1975-04-30       3.106105 -6.468717
# 1975-05-31       3.974628 -5.514316

print()
print('corr')
print(HPI.corr())
# strong negative correlation- as mortgage interest rates increase hpi housing price index decreases
# corr
#                United_States       M30
# United_States       1.000000 -0.778396
# M30                -0.778396  1.000000

state_HPI_M30 = HPI_data.join(m30)
print('state_HPI_M30 corr')
state_HPI_M30_corr = state_HPI_M30.corr()
print(state_HPI_M30_corr)
# state_HPI_M30 corr
#            ID        MN        OR        WA       M30
# ID   1.000000  0.969281  0.994960  0.994941 -0.767792
# MN   0.969281  1.000000  0.970385  0.973255 -0.765597
# OR   0.994960  0.970385  1.000000  0.996621 -0.790943
# WA   0.994941  0.973255  0.996621  1.000000 -0.791440
# M30 -0.767792 -0.765597 -0.790943 -0.791440  1.000000

print()
print('select row index and last column')
state_HPI_M30_corr_M30 = state_HPI_M30_corr['M30']
print(state_HPI_M30_corr_M30)
# select row index and last column
# ID    -0.767792
# MN    -0.765597
# OR    -0.790943
# WA    -0.791440
# M30    1.000000
# Name: M30, dtype: float64

print()
print(state_HPI_M30_corr_M30.describe())
# count    5.000000
# mean    -0.423154
# std      0.795662
# min     -0.791440
# 25%     -0.790943
# 50%     -0.767792
# 75%     -0.765597
# max      1.000000
# Name: M30, dtype: float64

print()
print('drop m30 row')
state_HPI_M30_corr_M30_drop_M30 = state_HPI_M30_corr_M30.drop(['M30'])
print(state_HPI_M30_corr_M30_drop_M30.describe())
# drop m30 row
# count    4.000000
# mean    -0.778943
# std      0.014173
# min     -0.791440
# 25%     -0.791067
# 50%     -0.779368
# 75%     -0.767243
# max     -0.765597
# Name: M30, dtype: float64
