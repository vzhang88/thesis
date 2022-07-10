from slide_completion import *

def sim_one_module():
    file = 'events_processed.csv'
    df = filter(file)

    # The number of slides in the module (+1 to account for 0-indexing)
    num_slides = df["slide_no"].max() + 1  
    print("The number of slides in the module is {}".format(num_slides))

    problem_slides = get_problem_slides(df)

    # Sanity check to check how many people completed a particular slide
    problem_df = df[(df.event_name == "problem_passed") & (df.slide_no == problem_slides[0])] # useful check
    print("The number of students which completed the first problem slide is {}".format(len(problem_df["user_id"].unique())))

    # Sort the dataset by users 
    df = df.sort_values(by=['user_id'])  
    student_dict = {}

    # Check the number of students in the dataset 
    num_students = len(df["user_id"].unique())
    print("The number of students is {}".format(num_students))
    
    student_dict = get_student_dict(df, num_slides, problem_slides)
    outcomes_dict, sequences_dict = get_results_dicts(student_dict, problem_slides)
    final_outcomes_dict, final_sequences_dict = aggregate(outcomes_dict, sequences_dict, num_students)
    plot_results(final_outcomes_dict, final_sequences_dict)

def main():
    sim_one_module()
    
if __name__ == "__main__":
    main()