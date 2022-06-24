from matplotlib import interactive
import pandas as pd 
import os
from dask import dataframe as dd
import matplotlib.pyplot as plt
import numpy as np
import os

from sklearn.metrics import jaccard_score
os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data")


# Filters dataset based on pre-defined filter 
def filter(file):
    df = pd.read_csv(file)
    filtered_df = df[(df.challenge_name == "challenge-newbies-2018")] 
    return filtered_df


# Returns dictionary of students; keys are student IDs and  values are another dictionary where 
# keys are problems attempted by student and values are events completed by student
def get_student_problem_interactions(file):
    # Filtered dataset
    df = filter(file)

    # Dictionary that will be returned
    students = {} 

    # Iterate through rows of filtered dataset
    for row in df.itertuples():

        # Retrieve name of current student 
        current_student = row.user_id
        if current_student not in students:
            students[current_student] = {}
        
        # Retrieve name of current problem  
        problem_name = row.challenge_name + row.problem_name
        if problem_name not in students[current_student]:
            students[current_student][problem_name] = []

        # Assign event to list corresponding to current problem
        students[current_student][problem_name].append(row.event_name)

    return students


# Returns information and statistics about dataset
def get_stats(file):
    pass


# Filters the student dictionary based on interaction sequences
def function(students):
    count = 0
    student_dist = {}
    problems = {}
    challenges = {}
    for student in students:
        for problem in students[student]:

            # Default boolean values 
            run_problem = False
            slide_view = False
            slide_complete = False
            problem_passed = False
            problem_failed = False

            # Retrieve challenge name
            split = problem.split("20")
            challenge = split[0] + "20" + split[1][1]


            # Change boolean values 
            for event in students[student][problem]:
                if event == "problem_run":
                    run_problem = True
                elif event == "slide_view":
                    slide_view = True
                elif event == "slide_steps_complete":
                    slide_complete = True
                elif event == "problem_passed":
                    problem_passed = True
                elif event == "problem_failed":
                    problem_failed = True

                # Modify the filter 
                if run_problem and not slide_view:
                    count += 1
                    if student not in student_dist:
                        student_dist[student] = 1
                    else:
                        student_dist[student] += 1
                    if problem not in problems:
                        problems[problem] = 1
                    else:
                        problems[problem] += 1
                    if challenge not in challenges:
                        challenges[challenge] = 1
                    else:
                        challenges[challenge] += 1
                    break 

    return student_dist, problems


def simulation(file):
    # Filtered dataset
    df = filter(file)

    # Dictionary that will be returned
    slides = {} 
    slides_success = {}
    success_users = []

    # Iterate through rows of filtered dataset
    for row in df.itertuples():
        if row.event_name == "slide_steps_complete":
            if row.slide_no not in slides:
                slides[row.slide_no] = []
            slides[row.slide_no].append(row.user_id)
        elif row.event_name == "problem_passed":
            if row.user_id not in success_users:
                success_users.append(row.user_id)
            if row.slide_no not in slides_success:
                slides_success[row.slide_no] = []
            if row.slide_no < 7:
                print("REACH")
            
            # Check if student has passed after completing
            if row.slide_no in slides and row.user_id in slides[row.slide_no]:
                slides_success[row.slide_no].append(row.user_id)
            
    for slide_no in slides:
        slides[slide_no] = len(set(slides[slide_no]))

    for slide_no in slides_success:
        slides_success[slide_no] = len(set(slides_success[slide_no]))

    #print("Number of users who passed the problem is:{}".format(len(success_users)))
    #plt.axhline(y=len(success_users), color='r', linestyle='-', label='Number of users who passed')

    plt.bar(slides.keys(), slides.values())
    plt.title("Slide Completion of Challenge-Newbies-2018-w5p2")

    #print(slides_success)
    #x_axis = np.arange(len(slides))
    #plt.bar(x_axis-0.2, slides.values(), width=0.4, label="Users who completed the slide")
    #plt.bar(x_axis+0.2, slides_success.values(), width=0.4, label="Users who completed and passed the slide")
    #plt.xticks(x_axis, slides)

    plt.legend()
    plt.xlabel('Slide number')
    plt.show()


def get_four_outcomes(df):
    original_df = df
    problem_names = ["w1p1", "w1p2", "w2p1", "w2p2", "w3p1", "w3p2", "w4p1", "w4p2", "w5p1", "w5p2"]
    for problem in problem_names:
        df = original_df[(original_df.problem_name == problem)] 
        student_outcomes_dict = {}
        for row in df.itertuples():
            if row.user_id not in student_outcomes_dict:
                student_outcomes_dict[row.user_id] = {}
                student_outcomes_dict[row.user_id][row.slide_no] = row.event_name

            else:
                student_outcomes_dict[row.user_id][row.slide_no] = row.event_name
                if student_outcomes_dict[row.user_id][row.slide_no] == "problem_passed":
                    continue

                elif student_outcomes_dict[row.user_id][row.slide_no]  == "problem_failed" and row.event_name == "problem_passed":
                    student_outcomes_dict[row.user_id][row.slide_no]  = row.event_name

        #print(student_outcomes_dict)

        problem_slides = []
        for student in student_outcomes_dict:
            for slide_no in student_outcomes_dict[student]:
                if student_outcomes_dict[student][slide_no] in ["problem_passed", "problem_failed"]:
                    problem_slides.append(slide_no)

        problem_slides = list(set(problem_slides))
        problem_slides = list(set(problem_slides))

        problem_slides.sort()
        
        if len(problem_slides) % 4 != 0:
            continue

        print(problem_slides)
        print(student_outcomes_dict)

        for student in student_outcomes_dict:
            slide_dict = student_outcomes_dict[student]
            i = problem_slides[0]
            j = problem_slides[1]
            k = problem_slides[2]
            l = problem_slides[3]

            if i in slide_dict and j in slide_dict:
                pass
                
            
            if k in slide_dict and l in slide_dict:  
                pass

        
        # print(hist_dict)
        # name = "Distribution of Outcomes for Problem {}".format(problem)
        # plt.title(name)
        # plt.xlabel("Outcomes")
        # plt.ylabel("Count")
        # plt.bar(hist_dict.keys(), hist_dict.values())
        # plt.savefig(name)
        # plt.show()


# def get_four_outcomes(df):
#     original_df = df
#     problem_names = ["w1p1", "w1p2", "w2p1", "w2p2", "w3p1", "w3p2", "w4p1", "w4p2", "w5p1", "w5p2"]
#     for problem in problem_names:
#         df = original_df[(original_df.problem_name == problem)] 
#         student_outcomes_dict = {}
#         for row in df.itertuples():
#             if row.user_id not in student_outcomes_dict:
#                 if row.event_name not in ["problem_passed", "problem_failed"]:
#                     student_outcomes_dict[row.user_id] = "Not attempted" # Have not run or submitted the code
#                 else:
#                     student_outcomes_dict[row.user_id] = row.event_name
#             else:
#                 if student_outcomes_dict[row.user_id] == "problem_passed":
#                     continue
#                 elif student_outcomes_dict[row.user_id] == "problem_failed" and row.event_name == "problem_passed":
#                     student_outcomes_dict[row.user_id] = row.event_name
#                 elif student_outcomes_dict[row.user_id] == "Not attempted" and row.event_name in ["problem_passed", "problem_failed"]:
#                     student_outcomes_dict[row.user_id] = row.event_name

#     #print(student_outcomes_dict)
    
#         hist_dict = {}
#         for student in student_outcomes_dict:
#             event_name = student_outcomes_dict[student]
#             if event_name not in hist_dict:
#                 hist_dict[event_name] = 1
#             else:
#                 hist_dict[event_name] += 1

#         print(hist_dict)
#         name = "Distribution of Outcomes for Problem {}".format(problem)
#         plt.title(name)
#         plt.xlabel("Outcomes")
#         plt.ylabel("Count")
#         plt.bar(hist_dict.keys(), hist_dict.values())
#         plt.savefig(name)
#         plt.show()


def main():
    file = 'events_processed.csv'
    df = filter(file)
    get_four_outcomes(df)

def plot_histograms(values):
    plt.hist(values)
    plt.show()


if __name__ == "__main__":
    main()











 