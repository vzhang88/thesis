from slide_completion import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import *
from sklearn.model_selection import *
import pandas as pd
from sklearn.linear_model import LogisticRegression
from general_functions import * 
from sklearn.dummy import DummyClassifier
from dropout import * 

# Uses the entire sequence - gets 84% accuracy - quite good!
def slide_value_prediction():
    df = pd.read_csv('all_results_grades.csv')
    sequences = get_sequences(df)
    slide_sequences = []
    for sequence in sequences:
        sequence = remove_all(sequence, "N")
        sequence = remove_all(sequence, "F")
        sequence = remove_all(sequence, "P")
        slide_sequences.append(sequence) # can try sequence[:40]

    X = np.array(slide_sequences)
    y = list(df["Grade"])
    y = np.array(y) 

    dummy_clf = DummyClassifier(strategy="most_frequent")
    lreg_clf = LogisticRegression(random_state=0, max_iter=1000) 

    base_score = get_cross_val_score(X, y, dummy_clf)
    ave_score = get_cross_val_score(X, y, lreg_clf)
    print(lreg_clf.classes_)
    importance = lreg_clf.coef_[2]
    # print(importance)

    # CLASSES - ['Early dropout' 'Late dropout' 'No dropout']
    # Note: .coef_ contains 3 lists - the first list are the 
    # strengths of each variable on the first class, so what we want
    # is to look at .coef_[2]

    importance_exp = np.exp(importance)
    # summarize feature importance
    for i,v in enumerate(importance_exp):
        # print('Feature: %0d, Score: %.5f' % (i,v))
        print('Feature: %0d, Score: %.5f' % (i,v))

    plt.bar([x for x in range(len(importance_exp))], importance_exp)
    plt.xlabel("Slide number")
    plt.ylabel("Slide importance in predicting final grade")
    plt.title("Slide importance distribution in predicting final grade")
    plt.show()
    print(base_score)
    print(ave_score)

 
def slide_value_prediction_with_problems():
    df = pd.read_csv('all_results_grades.csv')
    sequences = get_sequences(df)
    slide_sequences = []
    for sequence in sequences:
        sequence = remove_all(sequence, 0)
        sequence = remove_all(sequence, 1) 
        
        # Replace Ns with 0s, Fs with 1s and Ps with 2s 
        sequence[:] = [x if x != "N" else 0 for x in sequence]
        sequence[:] = [x if x != "F" else 1 for x in sequence]
        sequence[:] = [x if x != "P" else 2 for x in sequence]
        slide_sequences.append(sequence) # Only 40 problems, if we take first 25, we can predict with 91% accuracy

    X = np.array(slide_sequences)
    y = list(df["Grade"]) 
    y = np.array(y) 

    dummy_clf = DummyClassifier(strategy="most_frequent")
    lreg_clf = LogisticRegression(random_state=0, max_iter=1000, multi_class="multinomial") 
 
    base_score = get_cross_val_score(X, y, dummy_clf)
    ave_score = get_cross_val_score(X, y, lreg_clf)
    
    print(lreg_clf.classes_)
    importance_exp = np.exp(lreg_clf.coef_[2])

    for i,v in enumerate(importance_exp):
        # print('Feature: %0d, Score: %.5f' % (i,v))
        print('Feature: %0d, Score: %.5f' % (i,v))
    
    plt.bar([x for x in range(len(importance_exp))], importance_exp)
    plt.xlabel("Slide number")
    plt.ylabel("Slide importance in predicting dropout")
    plt.title("Slide importance distribution in predicting dropout")
    plt.show()
    print(base_score)
    print(ave_score)
