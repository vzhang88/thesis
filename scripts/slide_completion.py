from matplotlib import interactive
import pandas as pd 
import os
from dask import dataframe as dd
import matplotlib.pyplot as plt
import numpy as np
import os

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
    second_df = df[(df.slide_no < 5)]
    second_df.sort_values(by=['user_id'])
    student_dict = {}
    
    student = "3b9f1dbe452304fce7316bbb9734b7d3"
    student_dict[student] = []
    interaction_string = [0]*5
    previous_slide = None

    for row in second_df.itertuples():
        if row.user_id != student:
            if previous_slide == "problem":
                student_dict[student].append(interaction_string)
                interaction_string = [0]*5
            student = row.user_id
            student_dict[student] = []
            interaction_string = [0]*5
             
        if row.event_name == "slide_steps_complete":
            interaction_string[row.slide_no] = 1
            if previous_slide == "problem":
                student_dict[student].append(interaction_string)
                interaction_string = [0]*5
            previous_slide = "interactive"
             
        elif row.event_name == "problem_failed":
            interaction_string[row.slide_no] = 1
            previous_slide = "problem"

        elif row.event_name == "problem_passed":
            interaction_string[row.slide_no] = 2
            previous_slide = "problem"

    final_student_dict = {}
    for student in student_dict:
        if len(student_dict[student]) != 0 and [0,0,0,0,0] not in student_dict[student]:
            final_student_dict[student] = student_dict[student]

    outcomes_dict = {}
    sequences_dict = {}
    for student in final_student_dict:
        for entry in final_student_dict[student]:
            sequence = tuple(entry)
            if sequence not in sequences_dict:
                sequences_dict[sequence] = 0
            else:
                sequences_dict[sequence] += 1

            outcome = tuple(entry[-2:])
            if outcome not in outcomes_dict:
                outcomes_dict[outcome] = 0
            else:
                outcomes_dict[outcome] += 1

            # Tuples are hashable 

    print(outcomes_dict)
    print(sequences_dict)
    # Len(0) occurs when the row event name is neither of the three choices, and 
    # [0,0,0,0,0] occurs when the 

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







 