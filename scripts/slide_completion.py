from matplotlib import interactive
import pandas as pd 
import os
import matplotlib.pyplot as plt
import numpy as np
import os

# Key changes: We are only keeping one record of the interaction string for each student
# We are not holding multiple records that show the student's progression / slide completion order
# This will be captured by another type of encoding 

from sklearn.metrics import jaccard_score
os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")

# Filters dataset based on pre-defined filter 
def filter(file):
    df = pd.read_csv(file)
    filtered_df = df[(df.challenge_name == "challenge-newbies-2018") & (df.problem_name == "w1p1")] 
    return filtered_df

def main():
    file = 'events_processed.csv'
    df = filter(file)
    second_df = df[(df.slide_no < 13)] 

    # Sort the dataset by users 
    second_df.sort_values(by=['user_id'])
    student_dict = {}

    # Check the number of students in the dataset 
    print("The number of students is {}".format(len(second_df["user_id"].unique())))
    
    # The ID of the first student 
    student = "3b9f1dbe452304fce7316bbb9734b7d3"
    
    # The interaction string for each student 
    interaction_string = [0]*13

    student_dict[student] = interaction_string

    # Iterate through the rows of the dataframe
    for row in second_df.itertuples():

        # We have encountered a new student
        if row.user_id != student:

            # Assign the current student's ID to the student variable
            student = row.user_id

            # Construct a new zeroed interaction string and assign
            # it to the corresponding student entry in the dict
            interaction_string = [0]*13
            student_dict[student] = interaction_string

        # We have encountered a slide steps complete event
        if row.event_name == "slide_steps_complete":
            student_dict[student][row.slide_no] = 1

        elif row.event_name == "problem_failed":
            student_dict[student][row.slide_no] = 1

        elif row.event_name == "problem_passed":
            student_dict[student][row.slide_no] = 2

    # Dictionary to store the outcome tuples and their 
    # corresponding counts 
    outcomes_dict = {}

    # Dictionary to store the interaction sequences and their 
    # corresponding counts 
    sequences_dict = {}

    for student in student_dict:
        entry = student_dict[student] 
        sequence = tuple(entry)
        if sequence not in sequences_dict:
            sequences_dict[sequence] = 1
        else:
            sequences_dict[sequence] += 1
        outcome = tuple(entry[-2:]) 
        if outcome not in outcomes_dict:
            outcomes_dict[outcome] = 1
        else:
            outcomes_dict[outcome] += 1

    print(outcomes_dict)
    print(sequences_dict)

    plt.bar([str(key) for key in outcomes_dict.keys()], outcomes_dict.values())
    plt.title("Distribution of problem outcomes")
    plt.xlabel("Outcomes")
    plt.ylabel("Count")
    plt.show()

    plt.bar([str(key) for key in sequences_dict.keys()], sequences_dict.values())
    plt.title("Distribution of interaction sequences")
    plt.xlabel("Interaction sequence")
    plt.ylabel("Count")
    plt.show()
    
if __name__ == "__main__":
    main()







 