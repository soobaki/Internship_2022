{Compute missing feedback}

Before running this scripts make sure that you have python 3.6 or later.
Then install the packages needed by doing:

pip3 install -r requirements.txt

##############################################################################
All scripts have a command line interface so you can do --help to get more information, e.g.:

python3 compute_missing_feedback.py --help

##############################################################################
Important note:
    Do not forget to take in consideration how files paths are in each system.
    Windows use \
    While linux/mac use /


##############################################################################

Usage example:

mkdir output

python3 compute_missing_feedback.py --roster-path=roster.csv --feedback-path=feedback.csv --group-path=group.csv --output-dir='output'

roster.csv - complete roster of students (e.g., rostermissingfeedback2)
feedback.csv - submitted feedback (e.g., FA21-Sprint2CSCE431PeerFeedbackcomplete)
group.csv - Project group names and members (e.g., ProjectGroupsv8_old.csv)

**Make sure that all input files, especially the Project Group file (group.csv) is in CSV format and has a separate column called 'Groups' that store all the group names according to the student


OLD python3 compute_missing_feedback.py --roster-path=files/roster.csv --feedback-path=files/feedback.csv --output-dir='output'


Note: this will output the (last name of the student, the email address, UIN, and the last names of student feedbacks missing) of those with incomplete peer feedback
