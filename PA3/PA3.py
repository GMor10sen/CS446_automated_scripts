import zipfile
import os
import subprocess
import ast
import csv
from bs4 import BeautifulSoup
import re

#connect student's name with dowload folder name
def creat_id(folder_name):
    connect_dict = {}
    for file in os.listdir(folder_name):
        if file[-5:] == '.html':
            file_path = os.path.join(folder_name, file)
            soup = BeautifulSoup(open(file_path), 'html.parser')
            downloaded_name = soup.findAll('a')[0].get('href').split('threading-')[-1]
            downloaded_name = downloaded_name.split('.git')[0]
            downloaded_name = downloaded_name.split('/')[0]
            student_name = file.split('_')[0]
            connect_dict[downloaded_name] = student_name
    return connect_dict

def run_input(command):
    # Replace with the input string for the C program
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10, check=True)
        # Process the output from the C program
        stdout = result.stdout
        return stdout.decode()
    except subprocess.CalledProcessError as e:
        if e.returncode == subprocess.TimeoutExpired:
            result = None


def compare_test(stdout, answer_list):

    if stdout is None:
        return 0
    # Make a list to store output in
    output_list = stdout.lower()
    if answer_list.lower() in output_list:
        return 1

    return 0


### grade student score. Input folder dir, output a list of score [formats, main, commands, directories] and comments
def grade_stuent(folder_dir):
    questions, readfile, arraysumloop, arraySum_thread, arraySum_summation, arraySum_main = 0,6,13,5,5,13
    ###compile first:
    comment = ""
    if os.path.exists("./sumloop"):
        os.remove("./sumloop")
    if os.path.exists("./sumthread"):
        os.remove("./sumthread")

    if not os.path.exists(os.path.join(folder_dir, "loopedSummation.c")):
        readfile, arraysumloop = 0,0
    else:
        c_file_path = os.path.join(folder_dir, "loopedSummation.c")
        subprocess.call(["gcc", "-o", "sumloop", c_file_path, "-lpthread"])

    if not os.path.exists(os.path.join(folder_dir, "threadedSummation.c")):
        readfile, arraySum_thread, arraySum_summation, arraySum_main = 0,0,0,0
    else:
        c_file_path = os.path.join(folder_dir, "threadedSummation.c")
        subprocess.call(["gcc", "-o", "sumthread", c_file_path, "-lpthread"])

    if not os.path.exists("./sumloop"):
        return [0, 0, 0, 0, 0, 0], "loopedSummation.c file not exist or can't compile"
    if not os.path.exists("./sumthread"):
        return [0, 0, 0, 0, 0, 0], "threadedSummation.c file not exist or can't compile"

    #### test case 1
    command1 = ["./sumloop", "data.txt"]
    output_1 = run_input(command1)
    if output_1 is None:
        comment += "loopedSummation.c ignore the case when inputfile is incorrect; "

        readfile -= 1


    #### test case 2
    command1 = ["./sumloop"]
    output_1 = run_input(command1)

    if output_1 is None:
        comment += "loopedSummation.c ignore the case when inputfile is missing; "
        arraysumloop -= 1


    #### test case 3
    command1 = ["./sumloop", "number.txt"]
    output_1 = run_input(command1)
    if output_1 is None:
        arraysumloop  = 0
        comment += "loopedSummation.c error output; "
        return [questions, readfile, arraysumloop, arraySum_thread, arraySum_summation, arraySum_main], comment

    answer_list = "491281809"
    if compare_test(output_1, answer_list) == 0:
        comment += "loopedSummation.c sum result incorrect; "

        arraysumloop -= 5

    test_flag = True
    #### test case 4

    test_sum = 0
    test_time = 0
    for i in range(20):
        command1 = ["./sumthread","10","number.txt", "1"]
        output_1 = run_input(command1)
        if output_1 is None:
            arraySum_main = 0
            comment += "threadedSummation.c error output; "
            return [questions, readfile, arraysumloop, arraySum_thread, arraySum_summation, arraySum_main], comment

        output_2 = re.findall(r"\d+\.?\d*", output_1)
        if len(output_2) != 2:
            test_flag = False
            break

        test_sum += float(output_2[0])
        test_time += float(output_2[1])

    time_thread_10 = test_sum / 20
    test_time_10 = test_time / 20

    #### test case 5
    test_sum = 0
    test_time = 0
    for i in range(20):
        command1 = ["./sumthread", "40", "number.txt", "1"]
        output_1 = run_input(command1)
        if output_1 is None:
            arraySum_main = 0
            comment += "threadedSummation.c error output; "
            return [questions, readfile, arraysumloop, arraySum_thread, arraySum_summation, arraySum_main], comment

        output_2 = re.findall(r"\d+\.?\d*", output_1)
        if len(output_2) != 2:
            test_flag = False
            break

        test_sum += float(output_2[0])
        test_time += float(output_2[1])

    time_thread_40 = test_sum / 20
    test_time_40 = test_time / 20




    if not test_flag:
        arraySum_thread, arraySum_summation, arraySum_main = 0,0,0
        comment += "output error in threadedSummation.c"
    else:
        if time_thread_40 != 491281809 or time_thread_10 != 491281809:
            comment += "something wrong with the lock or sum process; "
            arraySum_main -= 5

        if test_time_40 <= test_time_10:
            comment += "pthread setting incorrect; "
            arraySum_thread -= 5

    #### test case 6

    command1 = ["./sumthread", "40", "number.txt"]
    output_1 = run_input(command1)
    if output_1 is None:
        comment += "ignore number of inputs in threadedSummation.c; "
        arraySum_main -= 1


    return [questions, readfile, arraysumloop, arraySum_thread, arraySum_summation, arraySum_main], comment

def write_results(students, grade, comments):
    # writing results to csv file
    with open('file.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        total = 0
        for i in range(6):
            total += grade[i]

        writer.writerow([students, grade[1], grade[2], grade[3], grade[4], grade[5], grade[0], total, comments])





def main():
    root_dir = './'
    path = root_dir + "PA3/Submissions"
    path2 = root_dir + "PA3/studentID"

    # if path already exists then do nothing, otherwise test students grade
    if not os.path.exists(path) or not os.path.exists(path2):

        print("Need to download submissions folder")

    else:
        name_list = creat_id(path2)


        with open('file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Studens', 'readfile', 'arraysumloop', 'arraySum_thread', 'arraySum_summation', 'arraySum_main', 'questions', 'Total Grade', 'Comments'])

        for repo_name in os.listdir(path):
            repo_dir = os.path.join(path, repo_name)
            if not os.path.isfile(repo_dir):
                if repo_name not in name_list.keys():
                    print(repo_name)
                else:
                    ## grading student
                    stuent_id = name_list[repo_name]
                    grade, comment = grade_stuent(repo_dir)
                    write_results(stuent_id,grade, comment)




        print("Grading Complete")



if __name__ == "__main__":
    main()








