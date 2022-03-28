import pandas as pd
import os
os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")
cwd = os.getcwd()
         
def convert_file(file):
    with open(file, encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile)
        df.to_csv(file.replace('json','csv'), encoding='utf-8', index=False)
            
def replace_json_with_csv(cwd):
    num_files = 0
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file.endswith(".json") and file != "events.json":
                absolute_path_to_file = root + "\\" + file
                convert_file(absolute_path_to_file)
                num_files += 1 
    print("The total number of files is: {}".format(num_files))

def delete_json_files(cwd):
    num_files = 0
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file.endswith(".json") and file != "events.json":
                os.remove(root + "\\" + file)
                num_files += 1 
    print("The total number of JSON files deleted is: {}".format(num_files))

def count_num_files(cwd):
    num_files = 0
    for root, dirs, files in os.walk(cwd):
        for file in files:
            num_files += 1
    print("The total number of JSON files deleted is: {}".format(num_files))

replace_json_with_csv(cwd)
delete_json_files(cwd)
count_num_files(cwd)



