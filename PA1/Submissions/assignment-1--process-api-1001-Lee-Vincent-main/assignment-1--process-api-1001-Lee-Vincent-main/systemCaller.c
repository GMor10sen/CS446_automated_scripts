/*
Author:         Vincent Lee
Instructor:     Sara Davis
Course:         CS 446: Operating Systems
Assignment:     Homework 1: CLI
Due Date:       6 Jan 2023
*/

// Macros

#define TRUE 1

// Libraries

#include <stdio.h> 
#include <string.h> 
#include <stdlib.h> 
#include <sys/wait.h> 
#include <sys/types.h> 
#include <unistd.h> 
#include <fcntl.h> 
#include <errno.h> 
#include <sys/stat.h> 


// Protoypes

int parseInput(char *, char *[]);
int executeCommand(char *[]);
void changeDirectories(char *);

// Main Driver

int main(int argc, char *argv[]) {
    while(TRUE) {
        // Display Prompt and Extract CLI
        printf("exampleShellvlee2$ ");
        fgets(argv[0], __INT_MAX__, stdin);

        // Parse CLI into 2D array and count args
        argc = parseInput(argv[0], argv);

        // If "exit" then end loop
        if(strcmp(argv[0], "exit") == 0)
            break;

        // If "cd" then check arg count, if correct then change directories
        if(strcmp(argv[0], "cd") == 0) {
            if(argc == 2)
                changeDirectories(argv[1]);
            else
                printf("Path Not Found!\n");
        }

        // Otherwise execute command and check for success
        else {
            if(executeCommand(argv) == 1)
                printf("Commmand Execution Failed!\n");
        }
    }
    return 0;
}


// Function Impl.

int parseInput(char *input, char *splitWords[]) {
    int wordInd = 0;
    splitWords[0] = strtok(input, " \r\n");
    while(splitWords[wordInd] != NULL) {
        splitWords[++wordInd] = strtok(NULL, " \r\n");
    }
    return wordInd;
}

int executeCommand(char *command[]) {
    pid_t status = fork();

    switch(status) {
        // Check for fork success
        case -1:
            printf("Fork Failed\n");
            return 1;

        // Execute command and check for success
        case 0:
            if(execvp(command[0], command) == -1)
                return 1;
        
        // Parent waits until children are done
        default:
            wait(&status);
            break;
    }

    return 0;
}

void changeDirectories(char *path) {

    // Check if moving up directory
    char *up = "..";
    if(strcmp(path, up) == 0) {
        chdir(path);
    }

    // Otherwise check for successful directory change
    else if(chdir(path) != 0) {
        printf("Path Not Found!\n");
    }
}
