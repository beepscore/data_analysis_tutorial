#!/usr/bin/env python3

# IO Basics - p.3 Data Analysis with Python and Pandas Tutorial
# https://pythonprogramming.net/input-output-data-analysis-python-pandas-tutorial/
# https://youtu.be/9Z7wvippeko

import pandas as pd

# quandl/zillow free data
# https://www.quandl.com/data/ZILLOW/Z77006_MLPAH-Zillow-Home-Value-Index-Zip-Median-Listing-Price-All-Homes-77006-Houston-TX

###
# To get info via api:
# install the Quandl Python Package
# import quandl

# For security keep quandl api key out of version control.
# e.g. read api key from command line argsv or from a file that is ignored.
# input_directory = "../data/input/"
# input_file_name = 'quandl_api_key.txt'
# input_file_path = input_directory + input_file_name
# rstrip to remove trailing \n
# quandl_api_key = open(input_file_path, 'r').read().rstrip()
# print('quandl_api_key', quandl_api_key)

# use quandl code ZILLOW/Z77006_MLPAH
# quandl.get("ZILLOW/Z77006_MLPAH", authtoken="authtoken")
# some requests don't need authtoken
# houses = quandl.get('FMAC/HPI_AK')
###

# for this tutorial, download a csv file locally to data/input/ZILLOW-Z77006_MLPAH.csv
# need quandl account to download file
# note pandas can import many formats e.g. csv, excel, html, json, sql, xml
# http://pandas.pydata.org/pandas-docs/stable/io.html

# path works from command line
# for PyCharm configuration set working directory to project root e.g.
# /Users/stevebaker/Documents/projects/pythonProjects/data_analysis_projects/data_analysis_tutorial
df = pd.read_csv("./data/input/ZILLOW-Z77006_MLPAH.csv")
print()
print('read read ZILLOW-Z77006_MLPAH.csv')
print(df.head())

# change index from default consecutive integers to Date column
# set_index returns a new dataframe, use inplace True to reassign df to new dataframe.
# alternatively could write df = df.set_index('Date')
# or df2 = df.set_index('Date')
df.set_index('Date', inplace=True)
print()
print('after set_index inplace=True')
print(df.head())
# output directory must exist, to_csv won't create one
df.to_csv("./data/output/zillow_date_index.csv")

# read output file (sic)
df = pd.read_csv("./data/output/zillow_date_index.csv")
print()
print('read zillow_date_index.csv')
# again pandas assigned default index, because a csv file doesn't have an attribute "index"
print(df.head())

# override default index
df = pd.read_csv("./data/output/zillow_date_index.csv", index_col=0)
print()
print('read set index_col=0')
print(df.head())

# rename columns
# index is not a column, don't include it in list
df.columns = ['Houston_HPI']
print('set columns')
print(df.head())

df.to_csv("./data/output/zillow_date_index_houston.csv")
df.to_csv("./data/output/zillow_date_index_houston_no_header.csv", header=False)
