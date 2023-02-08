import zipfile
import os
import subprocess 
import ast
import csv

def format_score(file_path):
    error_counter = 0 
    function_names = ["parseInput", "executeCommand", "changeDirectories"]
    
 
    with open(file_path, "r") as f:
        contents = f.read()
    
    for function_name in function_names:
        if f"{function_name}(" in contents:
            #print(f"Function '{function_name}' found in file ")
            error_counter = 0 
        else:
            #print(f"Function '{function_name}' not found in file")
            error_counter += 1
    
    if(error_counter == 0):
        return 10
    else:
        return 0
    
    
def run_input(file_path, input_str, answer_list, exact_factor):

   #compile student file 
    subprocess.call(["gcc", "-o", "studentprogram", file_path])

   # Run program
    process = subprocess.Popen('./studentprogram', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

   # Send multiple commands to the C program
    stdout, stderr = process.communicate(input_str.encode())

   # Remove example.c once created 
    if os.path.exists("example.c"):
        os.remove("example.c")
        print("File successfully removed")

   # Make a list to store output in 
    output_list = stdout.decode().split("\n")
    
   # Check if first 10 elements of list are equal to answer list 
    if output_list[0:exact_factor] == answer_list[0:exact_factor]:
        print("Lists are equal, program Success!")
        return 10
    else:
        print("Lists are not equal, Something went wrong...")
        return 0  
    




    
def main (): 
    path = "PA1/Submissions"

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

def grade_student(outer_path):
    
    #points formatted 
    students = []
    formats = [] 
    commands = []
    directories = []
    main = []

    student_count = 0
    #access c files within the directory of each students 
    for subdir, dirs, files in os.walk(outer_path):
       # print(files)
        for file in files:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and file.endswith(".c"):
                #get student id's 
                if (student_count < 90):
                    students.append(Obtain_Student(file_path))
                    #get formatting score 
                    formats.append(format_score(file_path))
                    #get main function behavior score 
                    input_str = 'ls\ntouch example.c\nls\nexit\n'
                    answer_list = "PA1\nPA2\nPA3\nPA4\nstudentprogram\nPA1\nPA2\nPA3\nPA4\nexample.c\n".split("\n")
                    main.append(run_input(file_path, input_str, answer_list, 10))
                    #get execute command behavior score 
                    commands.append(20)
                    #get directories behavior score 
                    input_str = 'cd PA1\nls\nexit\n'
                    answer_list = "Submissions\nauto.py".split("\n")
                    directories.append(run_input(file_path, input_str, answer_list, 2))

                student_count += 1 
             
    print("Ran though [", student_count ,"] students...")      
    write_results(students, formats, main, commands, directories)
                
def write_results(students, formats, main, commands, directories):
    # writing results to csv file
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Studens', 'Formating', 'Main', 'Commands', 'Directories', 'Total Grade'])
        for i in range(len(students)):
            grade = formats[i] + main[i] + commands[i] + directories[i]
            writer.writerow([students[i], formats[i], main[i], commands[i], directories[i], grade])

if __name__ == "__main__":
    main()