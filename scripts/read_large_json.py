import ijson
import os
import csv
os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")

user_to_repos = {}


f = open('events.csv', 'w', encoding='UTF8')
writer = csv.writer(f)
row_no = 0

with open("events.json", "r") as f:
    for record in ijson.items(f, "item"):
        if row_no == 0:
            row = list(record)
            row_no += 1
        else:
            row = list(record.values())
        writer.writerow(row)


