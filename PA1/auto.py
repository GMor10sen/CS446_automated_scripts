import zipfile
import os
import subprocess 
import ast

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
    
    
def main_behavor_score(file_path):
    success = 0
    print(file_path)
    subprocess.call(["gcc", "-o", "studentprogram", file_path])
    # Start the C program as a separate process
    process = subprocess.Popen(['./studentprogram'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # List of commands to be run in the C program
    commands = [
        "ls",
        "exit"
    ]

    # Send the commands to the C program's standard input stream and get its outputs
    for input_data in commands:
        output = process.communicate(input=input_data.encode())[0].decode()
        print(output)

    # Wait for the process to complete
    process.wait()

    return success

    
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
    #divide the string by the "\"'s 
    split_string = file_path.split("\\")

    # access the second item in the resulting list
    result = split_string[1]

    return result

def grade_student(outer_path):

    #points formatted 
    students = []
    formats = [] 
    commands = []
    directories = []
    main = []

    #access c files within the directory of each students 
    for subdir, dirs, files in os.walk(outer_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and file.endswith(".c"):
                #get student id's 
                students.append(Obtain_Student(file_path))
                #get formatting score 
                formats.append(format_score(file_path))
                #get main function behavior score 
                main.append(main_behavor_score(file_path))
                #get execute command behavior score 
                #commands.append(format_score(file_path))
                #get directories behavior score 
                #directories.append(format_score(file_path))
             
             
    #write_results(students, formats, main, commands, directories)
                
def write_results(students, formats, main, commands, directories):
    # writing results to csv file
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Studens', 'Formating', 'Main', 'Commands', 'Directories', 'Total Grade'])
        for i in range(len(str_list1)):
            grade = formats[i] + main[i] + commands[i] + directories[i]
            writer.writerow([students[i], formats[i], main[i], commands[i], directories[i], grade])

if __name__ == "__main__":
    main()