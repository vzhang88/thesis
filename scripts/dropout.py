import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import *
import pandas as pd
from sklearn.linear_model import LogisticRegression
from general_functions import * 
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from slide_completion import *

"""
    Determines the dropout class for all students in the challenge using their problem sequences
    and creates a new dataframe that contains the dropout class as well as the whole interaction sequence
    for all students
"""
def get_dropout_df(challenge_name):
    
    # Retrieve the problem sequences and interaction sequences for all students
    problem_sequence_dict, interaction_sequence_dict = get_interaction_dicts(challenge_name)

    # Create two lists to store all interaction sequences, and dropout statuses 
    # These lists represent separate columns in the dataframe 
    interaction_sequences = []
    statuses = []
     
     # Go through each student in the problem sequence dictionary 
    for student in problem_sequence_dict:
    
        # Convert the problem sequence from a list into a string 
        problem_sequence = "".join(problem_sequence_dict[student])

        # Count the number of characters that are not trailing Ns
        num = len(problem_sequence.rstrip("N"))

        # Determine the week at which the student drops out based
        # on the number of characters that are not trailing Ns 
        if 0 <= num and num <= 8:
            week = 1
        elif 9 <= num and num <= 16:
            week = 2
        elif 17 <= num and num <= 24:
            week = 3
        elif 25 <= num and num <= 32:
            week = 4
        elif 33 <= num and num < 40:
            week = 5
        else:
            week = "No dropout"

        # Determine the dropout status/class based on the week that students drop out
        if week == 1 or week == 2 or week == 3:
            status = "Early dropout"
        elif week == 4 or week == 5:
            status = "Late dropout"
        else:
            status = "No dropout"

        # Store the interaction sequence as a dictionary entry 
        interaction_sequences.append(interaction_sequence_dict[student])

        # Store the dropout status into the list of dropout statuses 
        statuses.append(status)

    # Prepare for dataframe creation 
    data = {"Student": list(interaction_sequence_dict.keys()), "Sequence":interaction_sequences, "Status":statuses}

    # Create the dataframe
    df = pd.DataFrame(data)

    # Save the dataframe 
    df.to_csv("dropout_df_{}.csv".format(challenge_name))


"""
    This function identifies whether the student drops out of the course based
    on their interaction sequence. The function does this by counting the number
    of consecutive Ns there are at the end of the string.
"""
def is_dropout(sequence):

    # Remove all interactive slide components 
    sequence.remove(0)
    sequence.remove(1)

    # Count the number of consecutive Ns at the end of the string 
    num_consecutive = 0
    for item in sequence:
        if item == "N":
            num_consecutive += 1
        else:
            num_consecutive = 0

    # There are consecutive Ns at the end of the string, indicating dropout 
    if num_consecutive > 0:
        return True
    else:
        return False


"""
    This function identifies and returns specific index (problem slide) at which the 
    student drops out (starts to record consecutive Ns) in the interaction sequence.
"""
def get_dropout_index(sequence):
    if not is_dropout(sequence):
        return -1
    elif "N" not in sequence:
        return -1
    else:
        return sequence.index("N")

        
"""
    This function calculates the 

"""
def get_dropout_module(sequence):

    # FF | FF | PP | NN | NN | NN 

    dropout_index = get_dropout_index(sequence)
    if dropout_index == -1:
        return -1
    else:
        return dropout_index/2 + 1


def get_dropout_dfs():
    challenges = ['challenge-newbies-2018', 'challenge-beginners-blockly-2018', 'challenge-beginners-2018', 'challenge-intermediate-2018']
    for challenge in challenges:
        get_dropout_df(challenge)


def dropout_prediction(challenge_name):
    
    os.chdir(r"C:\Users\vince\Documents\thesis\data\events")
    df = pd.read_csv('dropout_df_{}.csv'.format(challenge_name))
    sequences = get_sequences(df)

    for sequence in sequences:
        sequence[:] = [x if x != "N" else 0 for x in sequence]
        sequence[:] = [x if x != "F" else 1 for x in sequence]
        sequence[:] = [x if x != "P" else 2 for x in sequence]
        # sequence = sequence[:1]

    # Features 
    X = np.array(sequences)
    
    # Outcome 
    y = list(df["Status"])
    y = np.array(y)

    dummy_clf = DummyClassifier(strategy="most_frequent")
    lreg_clf = LogisticRegression(random_state=0, max_iter=1000, multi_class="multinomial") 
    nb_clf = GaussianNB()
    dt_clf = DecisionTreeClassifier()
    
    base_score = get_cross_val_score(X, y, dummy_clf)
    lreg_score = get_cross_val_score(X, y, lreg_clf)
    nb_score = get_cross_val_score(X, y, nb_clf)
    dt_score = get_cross_val_score(X, y, dt_clf)
     
    # Also print out base class 
    print(base_score)
    print(lreg_score)
    print(nb_score)
    print(dt_score)

# Somehow there are no dropouts 
challenge_name = "challenge-intermediate-2018"
dropout_prediction(challenge_name)