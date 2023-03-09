import zipfile
import os
import subprocess 
import ast
import csv
import glob

#main funciton for this autoscript which checks for a Submissions folder
def main (): 
    path = "PA2/Submissions"

    #if path already exists then do nothing, otherwise test students grade 
    if not os.path.exists(path):
            
      print("Need to download submissions folder")

    else: 
        #run through the submissions and grade each student 
        grade_student(path)
        
     
#obtain the student name ID 
def Obtain_Student(file_path): 

    # access the second item in the resulting list
    name = file_path.split("/")[2]

    return name




def ValuesOutput(py_file, cmd, expected, turn, wait):
    output = subprocess.run(cmd, stdout=subprocess.PIPE)

    output = str(output.stdout.decode())
        
    # Split the string into lines
    lines = output.splitlines()

    try:
        # Extract the lines that contain the values
        # Extract the values from the lines
        turnaround_time_line = [line for line in lines if "Turnaround Time:" in line][0]
        turnaround_time = turnaround_time_line.split(": ")[1]
    except IndexError:
        turnaround_time = "N/A"

    try:
        # Extract the lines that contain the values
        # Extract the values from the lines
        wait_time_line = [line for line in lines if "Wait Time:" in line][0]
        wait_time = wait_time_line.split(": ")[1] 
    except IndexError:
        wait_time = "N/A"


    # Extract the numbers from the lines
    numbers = [int(line) for line in lines if line.isdigit()]

    # Convert the numbers to a string
    result = "".join(map(str, numbers))



    # print("expected:", expected)
    # print("result:", result)
    # print("turnaround_time:", turnaround_time)
    # print("turn:", turn)
    # print("wait:", wait)
    # print()

    # Numbers should match expected 
    print(expected, "=?", result.strip(), " ", turn, "=?", turnaround_time.strip(), " ", wait, "=?", wait_time.strip())
    
   
    # 4 points provided for making it this far 
    points = 4
    errors = " "















    if (int(expected) == int(result.strip()) and float(turn) == float(turnaround_time.strip()) and float(wait) == float(wait_time.strip())):
        points = 4 + 6 #full points provided 
    else:
        if(int(expected) == int(result.strip())):
            points += 3
            errors += "calculation error"
        if(float(turn) == float(turnaround_time.strip())):
            points += 1.5
            errors += " turnaround time error"
        if (float(wait) == float(wait_time.strip())):
            points += 1.5
            errors += " wait time error"
   
    return points, errors


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
    ProgramRuns = [] 
    Main = []
    CalcStats = []
    ShortestJob = []
    RoundRobinSort = []
    BashScript = []
    Answers = [] 
    comments = []


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
                if(student_count < 2):
                    if(student_file.endswith(".sh")):
                        bash_file = student_file
                         #A bash script is successfully created and runs vmstat, top, and free and redirects their output to a txt file.
                        Keywords = ["free", "top", "vmstat", "free.txt", "vmstat.txt", "top.txt"]
                        search_bash(bash_file, Keywords)
                        BashScript.append(0)

                    if(student_file.endswith(".py")):
                        py_file = student_file
                        #if(Obtain_Student(py_file) != "2012-Williams-Daniel" and Obtain_Student(py_file) != "Quijano-Vanessa" ):
                        print("\nStudent:", Obtain_Student(py_file))

                        order = ["RoundRobin", "ShortestRemaining"]
                        ans = ["3172", "17123"] 
                        turn = ["65.25", "35.0"]
                        wait = ["43.75", "13.5"]

                        for i in range (2):
                            cmd = ["python3", py_file, os.path.join(path, directory, "pa2_batchfile.txt"), order[i]]

                            #print the output for the students code 
                            print(Output(py_file, cmd))

                            #calculate points and get error messages 
                            points, errors = ValuesOutput(py_file, cmd, ans[i], turn[i], wait[i])
                            print(points, " | ", errors)
                        

                        #Program runs without errors (no bugs)
                        ProgramRuns.append(0)

                        #A python main function is implemented(2); 
                        # all printing and reading is done from main (2),
                        # and data is then passed to and from other functions (2);
                        # logic to determine the correct algorithm to run is accurate (4)
                        Main.append(0)

                        # The averages are correctly calculated(4 pts), 
                        # and individual turnaround times (for each process) are calculated (3 pts). 
                        # The wait time for each process is accurately calculated (3 pts)
                        CalcStats.append(0)

                        # The function sorts each process by arrival time (2 pts) 
                        # and then checks what processes are available at each time (3),
                        # updates burst time when a process is interrupted(4),
                        # and breaks arrival time ties correctly (by PID)(1)
                        ShortestJob.append(0)

                        # The function sorts each process by arrival time (2 pts) 
                        # and then checks what processes are available (3),
                        # and executes the process with the lowest pid in the queue (1 for example) 
                        # for a full quanta (10 seconds) before executing the next(2).
                        # The process is repeated until all processes have fully executed 
                        # and the process run at each quanta is output to the screen (2)
                        RoundRobinSort.append(0)

                       
                        #There is no way to determine the .txt to my knowledge 
                        Answers.append(0)

                student_count += 1 

    print(student_count, " students total....")

    #write_results(students, ProgramRuns, Main, CalcStats, ShortestJob, RoundRobinSort, BashScript, Answers, comments)

# Creates the CSV file for the results           
def write_results(students, ProgramRuns, Main, CalcStats, ShortestJob, RoundRobinSort, BashScript, Answers, comments):
    # writing results to csv file
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Studens', 'ProgramRuns', 'Main', 'CalcStats', 'ShortestJob', 'RoundRobinSort', 'BashScript', 'Answers', 'Total Grade', 'Comments'])
        for i in range(len(students)):
            grade = ProgramRuns[i] + Main[i] + CalcStats[i] + ShortestJob[i] + RoundRobinSort[i] + BashScript[i] +  Answers[i]
            writer.writerow([students[i], ProgramRuns[i], Main[i], CalcStats[i], ShortestJob[i], RoundRobinSort[i],  BashScript[i],  Answers[i], grade, comments[i]])




#main force lock 
if __name__ == "__main__":
    main()

