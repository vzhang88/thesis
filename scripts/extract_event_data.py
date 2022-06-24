import pandas as pd
import os
import datetime
import csv

os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")
cwd = os.getcwd()


challenge_names = {}

with open('events_processed_10000.csv', 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["event_name", "created_at", "date_time", "user_id", "challenge_name", "problem_name", "week_no", "slide_no"])
    df = pd.read_csv('first_10000.csv')
    #for chunk in pd.read_csv('events.csv', chunksize=10000):
    for index, row in df.iterrows():
            event_data = row["event_data"]
            second_half = event_data.split("learn\/")[1]

            split = second_half.split("\/", 3)
            challenge_name = split[0]
            problem_name = split[1]
            slide_no = split[2]

            week_no = problem_name.split("p")[0]
            
            # CHALLENGES 
            if challenge_name not in challenge_names:
                challenge_names[challenge_name] = {}
            else:
                if problem_name not in challenge_names[challenge_name]:
                    challenge_names[challenge_name][problem_name] = {}
                else:
                    challenge_names[challenge_name][problem_name] = slide_no

            unix_time = row["created_at"]
            date_time = datetime.datetime.fromtimestamp(unix_time)
            date_time_formatted = f"{date_time:%Y-%m-%d %H:%M:%S}"

            csv_row = []
            csv_row.append(row["event_name"])
            csv_row.append(row["created_at"])
            csv_row.append(date_time_formatted)
            csv_row.append(row["user_id"])
            csv_row.append(challenge_name)
            csv_row.append(problem_name)
            csv_row.append(week_no)
            csv_row.append(slide_no)

            print(csv_row)
            writer.writerow(csv_row)


for problem_dicts in challenge_names.values():
    print(problem_dicts.keys())
    print(problem_dicts.values())


