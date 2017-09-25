#!/usr/bin/env python3

import pandas as pd

# tutorial 7 Pickline
# https://pythonprogramming.net/pickle-data-analysis-python-pandas-tutorial/

import pandas as pd
from matplotlib import style
import quandl

style.use('ggplot')

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
    """""
    return ['ID', 'OR', 'WA']


main_df = pd.DataFrame()

for abbreviation in us_states_short():
    query = "FMAC/HPI_" + str(abbreviation)

    # df = quandl.get(query, authtoken=quandl_api_key)
    # You have exceeded the API speed limit of 20 calls per 10 minutes. Please slow down your requests.
    df = quandl.get(query)

    # rename column 'Value' to abbreviation to avoid
    # ValueError: columns overlap but no suffix specified: Index(['Value'], dtype='object')

    df.rename(columns={'Value': str(abbreviation)}, inplace=True)

    if main_df.empty:
        main_df = df

    else:
        main_df = main_df.join(df)

print('main_df')
print(main_df)

#                    OR          WA
# Date
# 1975-01-31   19.688651   17.478975
# 1975-02-28   20.174137   17.544439
# 1975-03-31   20.634533   17.652704
# ...
# 2017-06-30  213.900185  216.341550
# [510 rows x 2 columns]
