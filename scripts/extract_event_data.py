import pandas as pd
import os
import datetime
import csv 
 
"""
    This method takes the events.csv file (converted to CSV from the original JSON file), and 
    creates eight columns representing key features for each record of the CSV file. Each
    record represents a user interaction with the platform, and has an event name, time of creation, 
    user ID etc. 
"""
def preprocess():

    with open('events_processed_20000.csv', 'w',  newline='') as f:

        # Create a writer to write to the new CSV file 
        writer = csv.writer(f)

        # Write the column names for the CSV file
        writer.writerow(["event_name", "created_at", "date_time", "user_id", "challenge_name", "problem_name", "week_no", "slide_no"])

        os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")
        df = pd.read_csv('events.csv')
        
        for row in df.itertuples():

            # Extract the event data 
            event_data = row.event_data
            second_half = event_data.split("learn\/")[1]

            split = second_half.split("\/", 3)
            challenge_name = split[0]
            problem_name = split[1]
            slide_no = split[2]

            # Extract the week number
            week_no = problem_name.split("p")[0]

            # Extract the unix time of the record 
            unix_time = row.created_at

            # Conver the unix time into the new datetime format
            date_time = datetime.datetime.fromtimestamp(unix_time)
            date_time_formatted = f"{date_time:%Y-%m-%d %H:%M:%S}"

            # Create the row to be written to the new CSV file
            csv_row = []
            csv_row.append(row.event_name)
            csv_row.append(row.created_at)
            csv_row.append(date_time_formatted)
            csv_row.append(row.user_id)
            csv_row.append(challenge_name)
            csv_row.append(problem_name)
            csv_row.append(week_no)
            csv_row.append(slide_no)
            writer.writerow(csv_row)
            break

def main():
    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")
    preprocess()

if __name__ == "__main__":
    main()