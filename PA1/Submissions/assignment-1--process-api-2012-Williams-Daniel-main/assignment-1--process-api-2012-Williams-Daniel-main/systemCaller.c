//Daniel Williams
//CS446: Intro to Operating Systems
//Programming Assignment 1: API
//Due: 1/6/2023 at 12:59 pm.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h> 
#include <sys/types.h>
#include <unistd.h>

#define TRUE 1
#define MAX_INPUT 50

int parseInput(char *input, char *splitWords[]);
int executeCommand(char *cdl[]);
void changeDirectories(char* dirName);

int main(){
    while(TRUE){
        printf(" exampleShelldanielwilliams$ ");
        char input[MAX_INPUT];
        fgets(input, MAX_INPUT, stdin);
        char *words[MAX_INPUT];
        int numArgs = parseInput(input, words);
        words[numArgs] = NULL;
        
        char except1[] = "cd";
        char except2[] = "exit";


        if(strcmp(words[0], except1) == 0){
            if(words[1] == NULL || words[2] != NULL){
                printf("Path Not Found!\n");
            }
            else{
                changeDirectories(words[1]);
            }
        }
        else if(strcmp(words[0], except2) == 0){
            break;
        }
        else{
            executeCommand(words);
        }
    }
}

int parseInput(char *input, char *splitWords[]){
    int wordInd = 0;
    splitWords[0] = strtok(input, " \n");
    while(splitWords[wordInd] != NULL){
        splitWords[++wordInd] = strtok(NULL, " \n");
    }
    return wordInd;
}

int executeCommand(char *cdl[]){
    if(cdl[0] != NULL){
        int pid = fork();
        if(pid < 0){
            printf("fork failed!");
            return 1;
        }
        else if(pid > 0){
            //int parentWait = (int)
            wait(NULL);
        }
        else{
            int success = execvp(cdl[0], cdl);
            if(success == -1){
                return 1;
            }
            return 0;
        }
    }
}

void changeDirectories(char* dirName){
    int cd = chdir(dirName);
    if(cd != 0){
        printf("Path Not Found!\n");
    }
}