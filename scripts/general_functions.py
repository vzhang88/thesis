from sklearn.model_selection import StratifiedKFold

"""
    Given a dataframe with a column "Sequence", containing all the interaction sequences associated with 
    each student in string format, this function converts the strings into their corresponding
    list form, and appends the list to a list of sequences

    Input: Dataframe 
    Returns: A list of interaction sequences for all students

"""
def get_sequences(df):
    sequences = []
    for l in df["Sequence"]:
        l = string_to_list(l)
        sequences.append(l)
    return sequences 


"""
    This function converts a string representation of a list into corresponding list form

    Input: Original string representation of the list 
    Returns: Converted list representation 
"""
def string_to_list(l):
    l = l.replace(",", "")
    l = l.replace("[", "")
    l = l.replace("]", "")
    l = l.replace("'", "")
    l = l.replace(" ", "")
    l = list(l)
    for i in range(len(l)):
        if l[i] == '0':
            l[i] = 0
        elif l[i] == '1':
            l[i] = 1
    return l
    

"""
    This function performs 10-fold cross-validation with stratification, and returns the average score. 
    
    When the classifier is a dummy classifier (ZeroR), we are evaluating the baseline success rate which gives us
    a floor value for the minimal value one's classifier should out-perform.

    Inputs: Xs (input vectors), ys (target vectors) an d clf (the classifier)
    Returns: Average score 
"""
def get_cross_val_score(X, y, clf):
    # List to store the scores for each fold 
    scores = []

    # Use 10-fold cross-validation with stratification 
    skf = StratifiedKFold(n_splits=10)
    for train_index, test_index in skf.split(X, y):

        # Retrieve the input and target samples 
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Evaluate the classifier 
        clf = clf.fit(X_train, y_train)

        # ADDITION
        y_target = clf.predict(X_test)
        print(y_target)
        num_correct = 0
        for i in range(len(y_target)):
            if y_target[i] == y_test[i] and y_target[i] == "Late dropout":
                num_correct += 1
        
        # Retrieve the score and append it to the scores list 
        # score = clf.score(X_test,y_test)
        y_test = y_test.tolist()
        score = num_correct / y_test.count("Late dropout")
        scores.append(score)
        
    ave_score = sum(scores)/len(scores)
    return ave_score 

"""
    Removes all occurences of a specified value 'val' in the given list, and returns
    a list without any 'val's
"""
def remove_all(the_list, val):
   return [value for value in the_list if value != val]