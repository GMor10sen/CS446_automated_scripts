import zipfile
import os
import subprocess
import ast
import csv
from bs4 import BeautifulSoup

#connect student's name with dowload folder name
def creat_id(folder_name):
    connect_dict = {}
    for file in os.listdir(folder_name):
        if file[-5:] == '.html':
            file_path = os.path.join(folder_name, file)
            soup = BeautifulSoup(open(file_path), 'html.parser')
            downloaded_name = soup.findAll('a')[0].get('href').split('cs446_pa1_sp23_cli-')[-1]
            student_name = file.split('_')[0]
            connect_dict[downloaded_name] = student_name
    return connect_dict

###### check question.txt (criteria 1) and get student's name
def answer_question(folder_dir):
    name = ""
    for file in os.listdir(folder_dir):
        if file == 'questions.txt':
            file_path = os.path.join(folder_dir, file)
            with open(file_path) as f:
                name = f.readline().strip().replace(" ","")
            if len(name) != 0:
                return name, 8
    return name, 0