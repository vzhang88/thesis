import ijson
import os
import csv
import pandas as pd 

"""
    Converts a large JSON file into an equivalent CSV file
"""
def read_large_json():

    # Create a file called events.csv 
    f = open('events.csv', 'w', encoding='UTF8')
    writer = csv.writer(f)
    row_no = 0

    # Read the events.json file
    with open("events.json", "r") as f:
        for record in ijson.items(f, "item"):
            if row_no == 0:
                row = list(record)
                row_no += 1
            else:
                row = list(record.values())

            # Write the row to the events.csv file 
            writer.writerow(row)


"""
    Creates a CSV version of the given JSON file 
"""
def convert_file(file):
    with open(file, encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile)
        df.to_csv(file.replace('json','csv'), encoding='utf-8', index=False)


"""
    Creates a CSV file for each JSON file in the current working directory 
"""     
def replace_json_with_csv(cwd):
    num_files = 0
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file.endswith(".json") and file != "events.json":
                absolute_path_to_file = root + "\\" + file
                convert_file(absolute_path_to_file)
                num_files += 1 
    print("The total number of files is: {}".format(num_files))


"""
    Deletes all JSON files within the current working directory 
"""
def delete_json_files(cwd):
    num_files = 0
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if file.endswith(".json") and file != "events.json":
                os.remove(root + "\\" + file)
                num_files += 1 
    print("The total number of JSON files deleted is: {}".format(num_files))


"""
    Counts the total number of files within the directory
"""
def count_num_files(cwd):
    num_files = 0
    for root, dirs, files in os.walk(cwd):
        for file in files:
            num_files += 1
    print("The total number of files is: {}".format(num_files))


def main():
    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")
    cwd = os.getcwd()
    replace_json_with_csv(cwd)
    delete_json_files(cwd)
    count_num_files(cwd)
    read_large_json()


if __name__ == "__main__":
    main()
