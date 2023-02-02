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
    print(file_path)
    subprocess.call(["gcc", "-o", "studentprogram", file_path])
    process = subprocess.Popen(["./studentprogram"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # # Provide input to the C program's standard input stream
    # input_data = "input data\n"
    # stdout, stderr = process.communicate(input=input_data.encode())

def main (): 
    path = "PA1/Submissions"

    #if path already exists then do nothing, otherwise test students grade 
    if not os.path.exists(path):
            
      print("Need to download submissions folder")

    else: 
        #run through the submissions and grade each student 
        grade_student(path)
        

     
def grade_student(outer_path):

    #access c files within the directory of each students 
    for subdir, dirs, files in os.walk(outer_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and file.endswith(".c"):
                #once c file is found begin tests : 
                
                #check if functions exist in c file 
                format_points = format_score(file_path)
                # run the C program and pass the input data
                main_points = main_behavor_score(file_path)
                
    


if __name__ == "__main__":
    main()