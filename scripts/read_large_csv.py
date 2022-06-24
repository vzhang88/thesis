import os
from dask import dataframe as dd
os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")

dask_df = dd.read_csv('events.csv')
df = dask_df.compute()
df.head(10000).to_csv('first_10000.csv')

 