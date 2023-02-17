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
    

    
def run_input(file_path, input_str):

    #compile student file 
    subprocess.call(["gcc", "-o", "studentprogram", file_path])

    # Run program with a 10 second timeout
    timeout_seconds = 10
    command = ['./studentprogram']

    # Replace with the input string for the C program
    try:
        result = subprocess.run(command, input=input_str.encode(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=timeout_seconds, check=True)
        # Process the output from the C program
        stdout = result.stdout
        return stdout
    except subprocess.CalledProcessError as e:
        if e.returncode == subprocess.TimeoutExpired:
            result = None
            
     

def compare_test(stdout, answer_list, exact_factor):
   # Remove example.c once created 
    if os.path.exists("example.c"):
        os.remove("example.c")
        #print("File successfully removed")

    if stdout is None:
        print("\n\n Error: Command did not work\n\n")  
        return 0
    # Make a list to store output in 
    output_list = stdout.decode().split("\n")
    

    while("" in output_list):
        output_list.remove("")

    output_string = str(stdout.decode()).lower()

    for elements in answer_list:
        if not (elements.lower() in output_string):
            return 0
        
    return 10 

    
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
    comments = []


    student_count = 0
    #access c files within the directory of each students 
    for subdir, dirs, files in os.walk(outer_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and file.endswith(".c"):
                #get student id's 
                print(Obtain_Student(file_path))

        
                if(student_count < 9000):
                    student_error = ''
                    if(student_count != 23 and student_count != 34 and student_count != 54 and  student_count != 60):

                        students.append(Obtain_Student(file_path))
                        # get formatting score 
                        formats.append(format_score(file_path))
                    
                        #get main function behavior score 
                        input_str = 'ls\ntouch example.c\nls\nexit\n'
                        answer_list = "PA1\nPA2\nPA3\nPA4\nstudentprogram\nPA1\nPA2\nPA3\nPA4\nexample.c\n".split("\n")
                        main_score = compare_test(run_input(file_path, input_str), answer_list, 10)
                        main.append(main_score)
                        
                        if(main_score == 0):
                            student_error += ", issue with 'touch' and 'ls' functionality"

                        #Command Function (auto pass)
                        commands.append(20)


                        #get directories behavior score 
                        input_str = 'cd PA1\nls\nexit\n'
                        answer_list = "Submissions\nauto.py".split("\n")
                        directory_score = compare_test(run_input(file_path, input_str), answer_list, 2)
                       

                        if(directory_score == 0):
                            student_error += ", issue with 'cd' functionality"


                        #check if there is an error message 
                        input_str = 'cd apple\nexit\n'
                        stdout = run_input(file_path, input_str)
                       
                        if stdout is not  None: 
                            output_list = str(stdout.decode()).lower()

                            # If it does not work 
                            if not ("not found" in output_list or "chdir failed" in output_list):
                                directories.append(max( (directory_score - 2) , 0))                                
                                student_error += ", no error messsage for incorrect cd"

                            else:
                                directories.append(directory_score)

                        else:
                            directories.append(max( (directory_score - 2) , 0)) 

                        # Add comment for specfic student 
                        comments.append(student_error)

                        print("\n\n\n=============", student_count, ") ", Obtain_Student(file_path), "=============\n\n\n")

                    student_count += 1 

    print(student_count, " students")

    # print("Ran though [", student_count ,"] students...")      
    write_results(students, formats, main, commands, directories, comments)
                
def write_results(students, formats, main, commands, directories, comments):
    # writing results to csv file
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Studens', 'Formating', 'Main', 'Commands', 'Directories', 'Total Grade', 'Comments'])
        for i in range(len(students)):
            grade = formats[i] + main[i] + commands[i] + directories[i]
            writer.writerow([students[i], formats[i], main[i], commands[i], directories[i], grade, comments[i]])

if __name__ == "__main__":
    main()