import zipfile
import os
import subprocess 
import ast

def search_for_functions(file_path, function_names):
    error_counter = 0 

    with open(file_path, "r") as f:
        contents = f.read()
    
    for function_name in function_names:
        if f"{function_name}(" in contents:
            print(f"Function '{function_name}' found in file ")
            error_counter = 0 
        else:
            print(f"Function '{function_name}' not found in file")
            error_counter += 1
    
    if(error_counter == 0):
        return 10
    else:
        return 0
    

def main (): 
    path = "PA1/Submissions"

    #if path already exists then do nothing, otherwise test students grade 
    if not os.path.exists(path):
            
        # Create an empty file 
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

    else: 

        #unzip the file containing all student submissions zips and place them in the empty file 
        zip_ref = zipfile.ZipFile("PA1/Archive.zip", 'r')
        zip_ref.extractall("PA1/Submissions")
        zip_ref.close()

        #Unzip each student zip file
        outer_path = "PA1/Submissions"
        for filename in os.listdir(outer_path):
            if filename.endswith(".zip"):
                inner_zip = zipfile.ZipFile(os.path.join(outer_path, filename), 'r')
                inner_zip.extractall(os.path.join(outer_path, filename[:-4]))
                inner_zip.close()
        grade_student(outer_path)
        

     
def grade_student(outer_path):

    #access c files within the directory of each students 
    for subdir, dirs, files in os.walk(outer_path):
        for file in files:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path) and file.endswith(".c"):
                #once c file is found begin tests : 
                function_names = ["parseInput", "executeCommand", "changeDirectories"]
                #check if functions exist in c file 
                format_score = search_for_functions(file_path, function_names)
    


if __name__ == "__main__":
    main()