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

                    if(student_file.endswith(".py")):
                       
                        #get the students python file as a variable 
                        py_file = student_file
                        student_name = Obtain_Student(py_file)
                        student_count += 1
                        
                        
                            
                        print("\nStudent:", student_name, student_count)
                        students.append(student_name)

                        order = ["RoundRobin", "ShortestRemaining"]
                        ans = ["1237123333", "17123"] 
                        turn = ["47.75", "35.0"]
                        wait = ["26.25", "13.5"]

                        calc_points = 0
                        round_points = 0
                        short_points = 0 

                        #students that break the code are skipped 
                        if(student_count != 25):
                            for i in range (2):
                                cmd = ["python3", py_file, os.path.join(path, directory, "pa2_batchfile.txt"), order[i]]

                                #print the output for the students code 
                                #print(Output(py_file, cmd))

                                #calculate points and get error messages 
                                num, act_num, turn_time, act_turn, wait_time, act_wait  = ValuesOutput(py_file, cmd, ans[i], turn[i], wait[i])
                                
                                #student calculated short or round correctly
                                if(num == act_num):
                                    if (i == 0):
                                        calc_points += 2
                                        # round_points += 10
                                    else:
                                        calc_points += 2
                                        # short_points += 10

                                #student did not get calculation correct 
                                else:
                                    if (i == 0):
                                        # round_points += 5
                                        calc_points += 1
                                        errors += " round calculation error"
                                    else:
                                        # short_points += 5
                                        calc_points += 1
                                        errors += " short calculation error"

                                #correct timearound time calculation 
                                if(turn_time == act_turn):
                                    calc_points += 1.5

                                else:
                                    if(i == 0):
                                        errors += " round calculation time error"
                                    if(i == 1):
                                        errors += " short calculation time error"

                                #correct wait time calculation 
                                if (wait_time == act_wait):
                                    calc_points += 1.5
                                else: 
                                    if(i == 0):
                                        errors += " round calculation wait error"
                                    if(i == 1):
                                        errors += " short calculation wait error"
    
                        #Program runs without errors (no bugs)
                        ProgramRuns.append(5)

                        #A python main function is implemented(2); 
                        # all printing and reading is done from main (2),
                        # and data is then passed to and from other functions (2);
                        # logic to determine the correct algorithm to run is accurate (4)
                        # if calculations work this will be true so assume full points 
                        Main.append(5)

                        # The averages are correctly calculated(4 pts), 
                        # and individual turnaround times (for each process) are calculated (3 pts). 
                        # The wait time for each process is accurately calculated (3 pts)
                        CalcStats.append(calc_points)

                        # The function sorts each process by arrival time (2 pts) 
                        # and then checks what processes are available at each time (3),
                        # updates burst time when a process is interrupted(4),
                        # and breaks arrival time ties correctly (by PID)(1)
                        RoundRobinSort.append(10) #assumed correct 

                        # The function sorts each process by arrival time (2 pts) 
                        # and then checks what processes are available (3),
                        # and executes the process with the lowest pid in the queue (1 for example) 
                        # for a full quanta (10 seconds) before executing the next(2).
                        # The process is repeated until all processes have fully executed 
                        # and the process run at each quanta is output to the screen (2)
                        ShortestJob.append(10) #assumed correct 

                       
                        #There is no way to determine the .txt to my knowledge 
                        Answers.append(0)

                        #add error comments 
                        comments.append(errors)

                

    print(student_count, " students total....")

    
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
    with open('Updatedpython.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Studens', 'ProgramRuns', 'Main', 'CalcStats', 'ShortestJob', 'RoundRobinSort', 'Answers', 'Total Grade', 'Comments'])
        for i in range(len(students)):
            grade = ProgramRuns[i] + Main[i] + CalcStats[i] + ShortestJob[i] + RoundRobinSort[i]  +  Answers[i]
            writer.writerow([students[i], ProgramRuns[i], Main[i], CalcStats[i], ShortestJob[i], RoundRobinSort[i],  Answers[i], grade, comments[i]])


def bash_results(students, Bash):
     
    # writing results to csv file
    with open('Updatebash.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Student', 'Bash'])
        for i in range(len(students)):
            writer.writerow([students[i], Bash[i]])




#main force lock 
if __name__ == "__main__":
    main()

