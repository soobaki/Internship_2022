import os

import pandas as pd
import argparse

# command prompt example in windows
# python3 compute_missing_feedback_test.py --roster-path="C:\Users\pobby\Desktop\feedback\rostermissingfeedback3.csv" --feedback-path="C:\Users\pobby\Desktop\feedback\FA21-Sprint2CSCE431PeerFeedbackcomplete.csv" --group-path="C:\Users\pobby\Desktop\feedback\ProjectGroupsv8_old.csv" --output-dir='output'

# parser to get user input from command prompt
parser = argparse.ArgumentParser(
    description='Compute missing feedback submissions. \n Usage: \n python3 compute_missing_feedback.py --roster-path=roster.csv --feedback-path=feedback.csv')
parser.add_argument('--roster-path', type=str, help='a path to the roosted csv, e.g. feedback/roster.csv')
parser.add_argument('--feedback-path', type=str, help='a path to the feedback csv, e.g. feedback/feedback.csv')
parser.add_argument('--group-path', type=str, help='a path to the feedback csv, e.g. feedback/projectgroup.csv')
parser.add_argument('--output-dir', type=str, default='.', help='output directory')

args = parser.parse_args()

roster_path = args.roster_path
feedback_path = args.feedback_path
group_path = args.group_path

# use pandas to read csv and store it into dataframe
roster_dataframe = pd.read_csv(roster_path)
feedback_dataframe = pd.read_csv(feedback_path)
group_dataframe = pd.read_csv(group_path)

# store group names in set to prevent duplicates
team = set(group_dataframe['Groups'])

# make a dictionary with key = team name and values = 0
team = dict.fromkeys(team, 0)

# assign number of people in a group as values in team dictionary
# cols is a list of the column 'Groups' in group_dataframe
cols = group_dataframe['Groups'].values.tolist()
for cell in cols:
    # increase the value in team dict by 1 if the program sees a group name
    team[cell] += 1

# we get the emails from the roster and make everything lowercase
all_emails = set((roster_dataframe['What is your TAMU email address?'].str.lower()))
submitted_emails = set((feedback_dataframe['What is your TAMU email address?'].str.lower()))

# not_submitted will be container for students who didn't submit every feedback
not_submitted = []
# make dictionary with key = every student's email and value = 0
actual = dict.fromkeys(all_emails, 0)

student_missing = []

# count how many feedbacks the student actually submitted and store it as the value in actual dict
for cell in feedback_dataframe['What is your TAMU email address?'].str.lower():
    actual[cell] += 1

# list the students who didn't receive the feedback
for student in all_emails:
    # get the index of the student's email in group_dataframe
    ind = group_dataframe[group_dataframe['What is your TAMU email address?'].str.lower() == student].index.values
    # get the student's group name
    student_team = list(group_dataframe.loc[ind, 'Groups'])
    student_team = ''.join(student_team)
    # get the index in group_dataframe where it has the same group name as the student
    team_ind = group_dataframe[group_dataframe['Groups'] == student_team].index.values
    # get teammates last name and first name from roster
    teammates_last = list(group_dataframe.loc[team_ind, 'What is your last name as it appears on the roster?'])
    # this list is made to store the raw data of group's first name from the group_dataframe (includes middle name as well in the first name)
    teammates_first_test = list(group_dataframe.loc[team_ind, 'What is your first name as it appears on the roster?'])
    teammates_first = []

    # for loop to chop up the middle name and only include the first name ex) John D -> John
    for first in teammates_first_test:
        x = first.split(' ')
        teammates_first.append(x[0])
    # this is made to check if student has a group or not later
    teammates_first_final = teammates_first.copy()
    teammates_last_final = teammates_last.copy()
    # temporarily created to use in a for loop
    teammates_first_1 = teammates_first.copy()
    teammates_last_1 = teammates_last.copy()
    # get student's name
    stu_ind = roster_dataframe[roster_dataframe['What is your TAMU email address?'].str.lower() == student].index.values
    stu_last = list(roster_dataframe.loc[stu_ind, 'What is your last name as it appears on the roster?'])
    # this list is made to store the raw data of student's first name from the roster_dataframe (includes middle name as well in the first name)
    stu_first_test = list(roster_dataframe.loc[stu_ind, 'What is your first name as it appears on the roster?'])
    stu_first = []
    for first in stu_first_test:
        x = first.split(' ')
        stu_first.append(x[0].lower())

    # can be deleted...? store student's first&last name by iterating through while loop and prevent storing students with the same first name ex)David Erdner and David Tang
    first_name = ""
    last_name = ""
    x=0
    while x < len(teammates_first_1):
        firstName = teammates_first_1[x]
        lastName = teammates_last_1[x]
        if firstName.lower() in stu_first:
            if lastName.lower() == stu_last[0].lower():
                first_name = firstName
                last_name = lastName
        teammates_first_1.remove(firstName)
        teammates_last_1.remove(lastName)

    x=0
    # while loop to remove the student from the teammates list b/c student should not evaluate themselves
    while x < len(teammates_first):
        firstName = teammates_first[x]
        lastName = teammates_last[x]
        if first_name == firstName:
            if last_name == lastName:
                teammates_first.remove(firstName)
                teammates_last.remove(lastName)
                x -= 1
        x += 1

    # save student's submitted feedback in submitted_feedback
    # get index where student submitted their feedback (two conditions: group name equals and email address equals)
    feedback_ind = feedback_dataframe[(feedback_dataframe['What is YOUR group name?'] == student_team) & (
            feedback_dataframe['Email Address'] == student)].index.values
    # get submitted feedback names
    submitted_feedback = list(
        feedback_dataframe.loc[feedback_ind, 'I am evaluating...(please DO NOT evaluate yourself)'])

    # empty list to store the first and last names of students that got their feedbacks
    feedback_last = []
    feedback_first = []
    # split up the name into first and last name ex) Legend, John D --> feedback_first = John & feedback_last = Legend
    for feedback in submitted_feedback:
        x = feedback.split(', ')
        feedback_last.append(x[0].lower())
        y = x[1].split(' ')
        feedback_first.append(y[0].lower())

    # while loop for removing students who didn't get their feedback from the lis
    x = 0
    while x < len(teammates_first):
        firstName = teammates_first[x]
        lastName = teammates_last[x]
        if firstName.lower() in feedback_first:
            if lastName.lower() in feedback_last:
                teammates_first.pop(x)
                teammates_last.pop(x)
                x -= 1
        x += 1

    # combine first and last name of students without feedback
    final_names = []
    for i in range(len(teammates_first)):
        final_names.append(teammates_first[i] + " " + teammates_last[i])

    # check if the student has any teammate -> if not, display no project group & if yes, display the names of students who didn't get their feedack from the student
    if len(teammates_first_final) == 0:
        teammates_first = "The student doesn't have a project group"
        teammates_last = ""
        not_submitted.append(student)
        student_missing.append(teammates_first)
    else:
        if len(teammates_first) != 0:
            not_submitted.append(student)
            student_missing.append(final_names)

# get the index of missing students based on email
# convert email to set and then back to list to prevent duplicates
not_submitted = list(set(not_submitted))
name_last = []
name_first = []
UIN = []

# get the student's first and last name and UIN from the roster_dataframe by index value of student's email
for final_stu in not_submitted:
    ind = roster_dataframe[roster_dataframe['What is your TAMU email address?'] == final_stu].index.values
    ind = ind[0]
    name_last.append(roster_dataframe._get_value(ind, 'What is your last name as it appears on the roster?'))
    name_first.append(roster_dataframe._get_value(ind, 'What is your first name as it appears on the roster?'))
    UIN.append(roster_dataframe._get_value(ind, 'What is your UIN?'))
ind = roster_dataframe['What is your TAMU email address?'].isin(not_submitted)
ind = list(ind[ind].index)

# combine the columns
df = {'first name': name_first,
      'last name': name_last,
      'email': not_submitted,
      'UIN': UIN,
      'Student(s) missing': student_missing
      }
print(df)
# make it into a dataframe
result = pd.DataFrame(df)

# put it in csv file called missing_feedback_result (can change name)
result.to_csv(os.path.join(args.output_dir, 'missing_feedback_result.csv'), index=False)
