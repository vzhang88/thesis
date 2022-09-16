import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import *
from sklearn.model_selection import *
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from general_functions import *
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

""""
    This function retrieves the challenge scores for the each student in the challenge 
    from the enrolments.csv file and adds an additional column to the dropout_df.csv 
    file which contains student IDs, their interaction sequences and their dropout statuses.
    The function also identifies students that do not have a score, and lists them as "Error"
    in the Score column.
"""
def get_scores():

    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\enrolments")
    enrolments_df = pd.read_csv("enrolments.csv")

    # Create a dictionary to store the final scores of students in the challenge
    student_final_score_dict = {}

    # Go through all entries in the enrolments file 
    for row in enrolments_df.itertuples():
        student_final_score_dict[row.user_id] = row.score

    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")
    dropout_df = pd.read_csv("dropout_df.csv")

    # Data to be converted into a dataframe 
    data = []

    # Go through all rows of the dropout dataframe file 
    for row in dropout_df.itertuples():
       
        # Dataframe row 
        r = []

        # Append the different column values to the dataframe row 
        r.append(row.Student)
        r.append(row.Sequence)
        r.append(row.Status)

        # Check if the student has a final score 
        if row.Student in student_final_score_dict:
            r.append(student_final_score_dict[row.Student])

        # Student doesn't have a final score, and so is an error case 
        else:
            print(row.Student)
            r.append("Error")

        # Append the row to the data list, which represents the dataframe 
        data.append(r)

    # Create a new dataframe with the following columns 
    new_df = pd.DataFrame(data, columns=["Student", "Sequence", "Status", "Score"])

    # Save the dataframe as a CSV file 
    new_df.to_csv("all_results.csv")


"""
    This function retrieves the grades for each student, using the scores 
    that are in "Scores" column of the all_results.csv file. THe function
    also adds an additional column representing the grades for each student.
    Ensure that all entries with "Error" are removed from all_results.csv
"""
def get_grades():

    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")

    # Read the dataframe with scores for each student 
    all_results_df = pd.read_csv("all_results.csv")

    # Data to be converted into a dataframe
    data = []

    sorted_scores = sorted(list(all_results_df['Score']))
    sorted_scores = remove_all(sorted_scores, 0)
    
    for row in all_results_df.itertuples():

        # Row of dataframe 
        r = []
        # Append the different column values to the row 
        r.append(row.Student)
        r.append(row.Sequence)
        r.append(row.Status)
        r.append(row.Score)

        # Convert the score into a grade, using the quartiles of the distribution of scores
        if row.Score == 0:
            grade = "N"

        elif row.Score < sorted_scores[len(sorted_scores)//4]: 
            grade = "D"

        elif sorted_scores[len(sorted_scores)//4] <= row.Score and row.Score < sorted_scores[len(sorted_scores)//2]:
            grade = "C"

        elif sorted_scores[len(sorted_scores)//2] <= row.Score and row.Score < sorted_scores[len(sorted_scores) * 3//4] :
            grade = "B"

        elif sorted_scores[len(sorted_scores) * 3//4] < row.Score:
            grade = "A"

        r.append(grade)

        # Append the row to the data list, which represents the dataframe
        data.append(r)

    # Create a new dataframe with the following columns 
    new_df = pd.DataFrame(data, columns=["Student", "Sequence", "Status", "Score", "Grade"])

    # Save the dataframe as a file, representing all scores and grade resulst 
    new_df.to_csv("all_results_grades.csv")


"""
    This function plots the distribution of the grades in the challenge 
"""
def get_grade_distribution():
    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")
    all_results_df = pd.read_csv("all_results_grades.csv")

    # Dictionary to store grade values and their counts 
    grade_dict = {}
    # Iterate through the rows of the dataframe 
    for row in all_results_df.itertuples():

        # Add to the count of the grade 
        if row.Grade not in grade_dict:
            grade_dict[row.Grade] = 1
        else:
            grade_dict[row.Grade] += 1
        
    # Plot the grade distribution 
    plt.bar(grade_dict.keys(), grade_dict.values())
    plt.xlabel("Grade")
    plt.ylabel("Count")    
    plt.title("Distribution of grades")
    plt.savefig("grade_distribution")
    plt.show()


"""
    This function predicts the grade for each student, and evaluates the accuracy, 
    comparing it to a base classifier
"""
# Grade prediction is hard to do (at least for challenge-newbies-2018)
def grade_prediction():
    
    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\events")
    df = pd.read_csv('all_results_grades.csv')
    sequences = get_sequences(df)

    # for sequence in sequences:
    #     sequence[:] = [x if x != "N" else 0 for x in sequence]
    #     sequence[:] = [x if x != "F" else 1 for x in sequence]
    #     sequence[:] = [x if x != "P" else 2 for x in sequence]

    # Features 
    # X = np.array(sequences)

    X = [l.count(0) for l in sequences]
    X = np.array(X).reshape(-1, 1)
    
    # Outcome 
    y = list(df["Grade"])
    y = np.array(y)

    dummy_clf = DummyClassifier(strategy="most_frequent")
    lreg_clf = LogisticRegression(random_state=0, max_iter=1000, multi_class="multinomial") 
    
    base_score = get_cross_val_score(X, y, dummy_clf)
    ave_score = get_cross_val_score(X, y, lreg_clf)
     
    print(base_score)
    print(ave_score)

