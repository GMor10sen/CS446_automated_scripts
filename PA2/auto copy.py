import zipfile
import os
import subprocess 
import ast
import csv
import glob

#main funciton for this autoscript which checks for a Submissions folder
def main (): 
    path = "Submissions"

    #if path already exists then do nothing, otherwise test students grade 
    if not os.path.exists(path):
            
      print("Need to download submissions folder")

    else: 
        #run through the submissions and grade each student 
        grade_student(path)
        
     
#obtain the student name ID 
def Obtain_Student(file_path): 

    # access the second item in the resulting list
    name = file_path.split("/")[1]

    return name


def ValuesOutput(py_file, cmd, expected, turn, wait):
    output = subprocess.run(cmd, stdout=subprocess.PIPE)

    output = str(output.stdout.decode())
  
    # print(output)
    # Split the string into lines
    lines = output.splitlines()

    try:
        # Extract the lines that contain the values
        # Extract the values from the lines
        turnaround_time_line = [line for line in lines if "Turnaround Time:" in line][0]
        turnaround_time = turnaround_time_line.split(": ")[1]
    except IndexError:
        turnaround_time = "0"

    try:
        # Extract the lines that contain the values
        # Extract the values from the lines
        wait_time_line = [line for line in lines if "Wait Time:" in line][0]
        wait_time = wait_time_line.split(": ")[1] 
    except IndexError:
        wait_time = "0"


    # Extract the numbers from the lines
    numbers = [int(line) for line in lines if line.isdigit()]

    # Convert the numbers to a string
    result = "".join(map(str, numbers))
    
    # If result is empty make 0 
    if (result == ''):
        result = 0
  
    print("exp: " , int(expected))
    print("act_res: " , int(result))
    print("turn: " , float(turn))
    print("act_turn: " , float(turnaround_time) )
    print("wait: " , float(wait))
    print("act_wait: " , float(wait_time) )

    return int(expected), int(result), float(turn), float(turnaround_time), float(wait), float(wait_time)


def Output(py_file, cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    return str(output.stdout.decode())
    
def search_bash(file, words):
    
    everything_contained = False

    with open(file, "r") as f:
        file_contents = f.read()
        
        everything_contained = all(word in file_contents for word in words)
        some_contained = any(word in file_contents for word in words)

    if(everything_contained):
        return 5
    elif(some_contained):   
        return 2.5
    else:
        return 0


def grade_student(path):
    
    #points formatted 
    students = []
    bash_studens = []
    ProgramRuns = [] 
    Main = []
    CalcStats = []
    ShortestJob = []
    RoundRobinSort = []
    BashScript = []
    Answers = [] 
    comments = []

    bash_value = 0
    student_count = 0
   # Iterate over each directory in the Submissions folder
    for directory in os.listdir(path):
        # Check if the directory is a subdirectory (i.e., not a file)
        if os.path.isdir(os.path.join(path, directory)):
            # Get a list of all .py files in the subdirectory
            py_files = glob.glob(os.path.join(path, directory, "*.py"))
             # Get a list of all .sh files in the subdirectory
            sh_files = glob.glob(os.path.join(path, directory, "*.sh"))
            # Print the student name and the name of each .py file
            for student_file in py_files + sh_files:
               
                
                if(True):
                 
                    errors = ' '
                    if(student_file.endswith(".sh")):
                        bash_studens.append(Obtain_Student(student_file))
                        #get the students bash file as a variable 
                        bash_file = student_file
                        bash_value += 1 
                        #A bash script is successfully created and runs vmstat, top, and free and redirects their output to a txt file.
                        Keywords = ["free", "top", "vmstat", "free.txt", "vmstat.txt", "top.txt"]
                        BashScript.append(search_bash(bash_file, Keywords))

                    
                

    print(student_count, " students total....", bash_value, "bash files...")

    write_results(students, ProgramRuns, Main, CalcStats, ShortestJob, RoundRobinSort, Answers, comments)
    bash_results(bash_studens, BashScript)

 
# Creates the CSV file for the results           
def write_results(students, ProgramRuns, Main, CalcStats, ShortestJob, RoundRobinSort, Answers, comments):
    print("====Data====")
    print(students)
    print(ProgramRuns)
    print(Main)
    print(CalcStats)
    print(ShortestJob)
    print(RoundRobinSort)
    print(Answers)
    print(comments)

    
    # writing results to csv file
    with open('python.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Studens', 'ProgramRuns', 'Main', 'CalcStats', 'ShortestJob', 'RoundRobinSort', 'BashScript', 'Answers', 'Total Grade', 'Comments'])
        for i in range(len(students)):
            grade = ProgramRuns[i] + Main[i] + CalcStats[i] + ShortestJob[i] + RoundRobinSort[i] + BashScript[i] +  Answers[i]
            writer.writerow([students[i], ProgramRuns[i], Main[i], CalcStats[i], ShortestJob[i], RoundRobinSort[i],  BashScript[i],  Answers[i], grade, comments[i]])


def bash_results(students, Bash):
     
    # writing results to csv file
    with open('bash.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Student', 'Bash'])
        for i in range(len(students)):
            writer.writerow([students[i], Bash[i]])

#main force lock 
if __name__ == "__main__":
    main()

