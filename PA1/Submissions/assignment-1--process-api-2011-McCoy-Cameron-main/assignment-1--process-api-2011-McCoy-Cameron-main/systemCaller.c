#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

void changeDirectories(char *inputParse[]);

int parseInput(char *input, char *splitWords[]);

int executeCommand(char *cli[]);

int main(int argc, char *argv[])
{
    int runState = 1;

    while (runState)
    {

        int myWordInd;
        char *parsedWords[100];
        char userInput[100];
        printf("exampleShellcameronm$ ");
        fgets(userInput, 100, stdin);
        myWordInd = parseInput(userInput, parsedWords);
        if (strcmp("exit", parsedWords[0]) == 0)
        {
            return 0;
        }
        else if (strcmp("cd", parsedWords[0]) == 0)
        {
            changeDirectories(parsedWords);
        }
        else
        {
            executeCommand(parsedWords);
        }
    }

    return 0;
}

int executeCommand(char *cli[])
{
    int status;
    int PID = fork();
    if (PID < 0)
    {
        printf("Fork failed!");
        return -1;
    }
    if (PID != 0)
    {
        while (waitpid(-1, &status, 0) != PID)
            ;
    }
    else
    {

        if (execvp(cli[0], cli) == -1)
        {
            printf("Fork failed! \n");
        }
        else
        {
            execvp(cli[0], cli);
        }
    }

    return 0;
}

int parseInput(char *input, char *splitWords[])
{

    int wordInd = 0;
    splitWords[0] = strtok(input, " \n");
    while (splitWords[wordInd] != NULL)
    {

        splitWords[++wordInd] = strtok(NULL, " \n");
    }
    return wordInd;
}

void changeDirectories(char *inputParse[])
{

    if (chdir(inputParse[1]) == -1)
    {
        printf("Path not found \n");
    }
    else
    {
        chdir(inputParse[1]);
    }
}