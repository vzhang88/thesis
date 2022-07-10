from matplotlib import interactive
import pandas as pd 
import os
import matplotlib.pyplot as plt
import numpy as np
import os

# Key changes
# In addition to the below, moved the simulations to a separate file 
# called slide_completion_sim.py. This file does not have a main function.
# 1) Fixed a major (I wasn't actually sorting the slides previously), so now
# the distributions are accurate
# 2) In addition, aggregated less frequently occuring outcomes 
# into an "Other" category. 
# 3) Changed the formatting of the interaction string: "P" for problem slide pass
# "F" for problem slide fail, and "N" for problem slide no attempt. 

from sklearn.metrics import jaccard_score
os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")

# Filters dataset based on pre-defined filter 
def filter(file):
    df = pd.read_csv(file)
    filtered_df = df[(df.challenge_name == "challenge-newbies-2018") & (df.problem_name == "w1p1")] 
    return filtered_df

def plot_results(final_outcomes_dict, final_sequences_dict):
    plt.bar([str(key) for key in final_outcomes_dict.keys()], final_outcomes_dict.values())
    plt.title("Distribution of problem outcomes")
    plt.xlabel("Outcomes")
    plt.ylabel("Count")
    plt.show()

    plt.bar([str(key) for key in final_sequences_dict.keys()], final_sequences_dict.values())
    plt.title("Distribution of interaction sequences")
    plt.xlabel("Interaction sequence")
    plt.ylabel("Count")
    plt.show()
    
# Aggregate all outcomes that do not appear as frequently
# into a separate category called "Other"
def aggregate(outcomes_dict, sequences_dict, num_students):
    final_outcomes_dict = {}
    for outcome in outcomes_dict:
        if outcomes_dict[outcome] < num_students/10:
            if "Other" not in final_outcomes_dict:
                final_outcomes_dict["Other"] = outcomes_dict[outcome]
            else:
                final_outcomes_dict["Other"] += outcomes_dict[outcome]
        else:
            final_outcomes_dict[outcome] = outcomes_dict[outcome]

    # Aggregate all sequences that do not appear as frequently
    # into a separate category called "Other"
    final_sequences_dict = {}
    for sequence in sequences_dict:
        if sequences_dict[sequence] < num_students/10:
            if "Other" not in final_sequences_dict:
                final_sequences_dict["Other"] = sequences_dict[sequence]
            else:
                final_sequences_dict["Other"] += sequences_dict[sequence]
        else:
            final_sequences_dict[sequence] = sequences_dict[sequence]

    return final_outcomes_dict, final_sequences_dict


def get_results_dicts(student_dict, problem_slides):
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
        
        # Indices of the first pair of problem slides 
        idx0 = problem_slides[0]
        idx1 = problem_slides[1]
        
        # Indices of the second pair of problem slides 
        idx2 = problem_slides[2]
        idx3 = problem_slides[3]

        outcome = tuple(entry[idx0:idx1+1] + entry[idx2:idx3+1]) 
        if outcome not in outcomes_dict:
            outcomes_dict[outcome] = 1
        else:
            outcomes_dict[outcome] += 1
    
    return outcomes_dict, sequences_dict

def get_student_dict(df, num_slides, problem_slides):
    student_dict = {}
    # The ID of the first student 
    student = df.iloc[0].user_id

    # The interaction string for each student 
    interaction_string = [0]*num_slides
    for slide_no in problem_slides:
        interaction_string[slide_no] = "N"

    student_dict[student] = interaction_string

    # Iterate through the rows of the dataframe
    for row in df.itertuples():

        # We have encountered a new student
        if row.user_id != student:

            # Assign the current student's ID to the student variable
            student = row.user_id

            # Construct the default interaction string for each student
            # This consists of 0s where there is an interaction slide
            # and Ns where there is a problem slide 
            interaction_string = [0]*num_slides
            for slide_no in problem_slides:
                interaction_string[slide_no] = "N"

            student_dict[student] = interaction_string

        # We have encountered a slide steps complete event
        if row.event_name == "slide_steps_complete" and row.slide_no not in problem_slides: # Check how many of these there are 
            student_dict[student][row.slide_no] = 1

        elif row.event_name == "problem_failed" and row.slide_no in problem_slides:
            # Only update the slide's status to fail if the student had not 
            # already passed the slide before 
            if student_dict[student][row.slide_no] != "P":
                student_dict[student][row.slide_no] = "F" 

        elif row.event_name == "problem_passed" and row.slide_no in problem_slides:
            student_dict[student][row.slide_no] = "P" 

    return student_dict

def get_problem_slides(df):
    # Problem slides containing the slide numbers of the designated problems 
    problem_slides = []
    problem_df = df[(df.event_name == "problem_passed")] # This is a useful check 
    for slide_no in problem_df["slide_no"].unique():

        # Note: Some interactive slides are mislabelled as problem slides. To account
        # for this, take the problem slides that have a high rate of visits from users
        if len(problem_df[(problem_df.slide_no == slide_no)]) > 500:
            problem_slides.append(slide_no)
    problem_slides.sort()
    print("The problem slides are {}".format(problem_slides))
    return problem_slides


 

 