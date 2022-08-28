import pandas as pd 
import os
import matplotlib.pyplot as plt

"""
    This function provides a summary of the dataset. Specifically, 
    it produces a bar graph showing the compositional breakdown of
    participants overall and the distribution of participants across
    different challenges
"""
def get_dataset_summary():
    
    os.chdir(r"C:\Users\vince\Documents\thesis\data\raw_data\enrolments")

    print("SUMMARY OF DATASET")

    # Read the enrolments file, which contains records of each student's enrolment, 
    # in a challenge, as well as other student characteristics 
    # such as their final grade in the challenge
    df = pd.read_csv('enrolments.csv')

    os.chdir(r"C:\Users\vince\Documents\thesis\results\dataset_results")

    # Note: There are a number of teachers, professional sand pre-service teachers
    # These should be removed, as we are solely interested in students
    print(df['role'].value_counts())

    # Remove teachers, professionals and pre-service teacher from dataset 
    df = df[df['role'] != 'Teacher']
    df = df[df['role'] != 'Professional']
    df = df[df['role'] != 'Pre-service teacher']

    # No. of records
    num_records = len(df)
    print("The number of enrolment records is {}".format(num_records))

    num_students = len(df["user_id"].unique())
    print("The number of students is {}".format(num_students))

    # There are four challenges that we are interested in 
    # challenge-beginners-2018
    # challenge-beginners-blockly-2018
    # challenge-newbies-2018 
    # challenge-intermediate-2018

    # Plot student enrolment across challenges
    challenges = list(df['course'].unique())

    # Dictionary storing challenges as keys and the number
    # of students enrolled as values
    challenge_dict = {}
    for row in df.itertuples():
        challenge = row.course
        if challenge not in challenge_dict:
            challenge_dict[challenge] = 1
        else:
            challenge_dict[challenge] += 1

    plt.bar(challenge_dict.keys(), challenge_dict.values())
    plt.xlabel("Challenge")
    plt.ylabel("Number of students enrolled")
    plt.title("Student enrolment across challenges")
    plt.savefig("student_enrolment_across_challenges")
    plt.show()
    
    # Create a figure containing four sublots for those four challenges 
    fig, ax = plt.subplots(2, 2, sharey=True)

    # Subplot indices
    i = 0 
    j = 0 

    challenges.remove('challenge-advanced-2018')
    print("The challenges include: {0}, {1}, {2} and {3}".format(*challenges,))

    for challenge in challenges:
        filter_df = df[(df.course==challenge)]

        # Plot a histogram of the final score, using bins of width 10
        ax[i, j].hist(list(filter_df['score']), 10)

        # Set the title for the histogram
        ax[i, j].set_title("Distribution of final scores for {}".format(challenge))

        # Move to the next subplot
        j += 1 
        if j == 2:
            j = 0
            i += 1

    for a in ax.flat:
        a.set(xlabel='Final score', ylabel='Frequency')
        
    for a in ax.flat:
        a.label_outer()

    fig.suptitle("Distribution of final scores across challenges")
    plt.savefig("distribution_of_final_scores_across_challenges")
    plt.show()

def main():
    get_dataset_summary()

if __name__ == "__main__":
    main()