import os
import pandas as pd

os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")

df = pd.read_csv("events.csv")

head = df.head(1000)
head.to_csv("first_1000.csv")