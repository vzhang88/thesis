
from slide_completion import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import *
from sklearn.model_selection import *
import pandas as pd
from sklearn.linear_model import LogisticRegression
from general_functions import * 
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from dropout import * 


"""
    This function predicts the final outcome for each module (outcome of the final problem) 
    in a given challenge using all preceding slides in the module (interactive and problem slides), 
    and evaluates the accuracy of the prediction against a base classifier. If there are two 
    final problems in a module, then this problem uses all slides preceding the paired problems
    (i.e. it excludes the first of the paired problems)
"""
def module_prediction():

    file = 'events_processed.csv'
    challenge_name = "challenge-newbies-2018"
    df = pd.read_csv(file) 

    # Module names 
    problem_names = ["w1p1", "w1p2", "w2p1", "w2p2", "w3p1n", "w3p2", "w4p1", "w4p2", "w5p1", "w5p2"]
 
    # Data to be converted into a dataframe 
    data = []

    # GO through each of the modules 
    for problem_name in problem_names: 

        # Inputs
        X = []
        # Outcomes 
        y = []

        # Filter the dataframe based on challenge name and module name 
        df = filter(file, challenge_name, problem_name)

        # The number of slides in the module (+1 to account for 0-indexing)
        num_slides = df["slide_no"].max() + 1  
        problem_slides = get_problem_slides(df, challenge_name)

        # Sort the dataset by users 
        df = df.sort_values(by=['user_id'])  
        
        # Retrieve the interaction sequences of each student in the module 
        temp_dict = get_student_dict(df, num_slides, problem_slides)

        # Last problem slide 
        last_idx = problem_slides[-1] 

        # Go through all students in the module 
        for student in temp_dict:

            # Row of the dataframe 
            row = []

            # Retrieve the student's interaction sequence 
            sequence = temp_dict[student]

            # Replace all Ns with 0s and Fs with 1s and Ps with 2s
            sequence[:] = [x if x != "N" else 0 for x in sequence]
            sequence[:] = [x if x != "F" else 1 for x in sequence]
            sequence[:] = [x if x != "P" else 2 for x in sequence]

            # The outcome is the outcome of the last problem slide in the module 
            outcome = sequence[last_idx] 

            # Append the outcome to the list of outcomes 
            y.append(outcome)

            # Remove the last problem from the sequence 
            sequence.pop(last_idx)

            # If problems come in pairs, we expect that the first problem may be a predictor of the next, 
            # and so get rid of the first problem from the list - potentially, get rid of all problems 
            if problem_slides[-2] == last_idx - 1:
                sequence.pop(last_idx - 1)

            # Store the remaining sequence in the inputs vector 
            X.append(sequence)

            # Append the sequence to the row
            row.extend(sequence)

            # Append the outcome to the row vector 
            row.append(outcome)

            # Append the row to the dataframe 
            data.append(row)

        # df = pd.DataFrame(data)
        dummy_clf = DummyClassifier(strategy="most_frequent")
        lreg_clf = LogisticRegression(random_state=0, max_iter=1000, multi_class="multinomial") 
        nb_clf = GaussianNB()
        dt_clf = DecisionTreeClassifier(random_state=0)
        
        X = np.array(X)
        X.reshape(1, -1)
        y = np.array(y)
    
        # Calculate the cross-validated scores for the base classifier, logistic regressio nclassifier, navie Bayes 
        # colassifier and decision tree classifeir 
        base_score = get_cross_val_score(X, y, dummy_clf)
        lreg_score = get_cross_val_score(X, y, lreg_clf)
        nb_score = get_cross_val_score(X, y, nb_clf)
        dt_score = get_cross_val_score(X, y, dt_clf)

        print("The base score for {} is: {}".format(problem_name, base_score))
        print("The average score for {} is: {}".format(problem_name, lreg_score))
        print("The average score for {} is: {}".format(problem_name, nb_score))
        print("The average score for {} is: {}".format(problem_name, dt_score))

        importance_exp = np.exp(lreg_clf.coef_[0])

        for i,v in enumerate(importance_exp):
            # print('Feature: %0d, Score: %.5f' % (i,v))
            print('Feature: %0d, Score: %.5f' % (i,v))
        
        plt.bar([x for x in range(len(importance_exp))], importance_exp)
        plt.xlabel("Slide number")
        plt.ylabel("Slide importance in predicting dropout")
        plt.title("Slide importance distribution in predicting dropout")
        plt.show()
        print("\n")

module_prediction()