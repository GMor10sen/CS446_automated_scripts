**<p align = "center"> CS446-Winter23-PA1</p>**

**Learning Outcomes**
1. You will implement the general system process call API in C using fork, wait, and execvp. 
2. You will be able to describe how Unix implements general process execution of a child from a parent process.
3. You will write a shell program in C so that you can see how child processes are created and destroyed &  how they interact with parent processes.<br/>

**General Instructions and Hints**: 

-The code for this assignment _must_ be in C.<br/>
-There is a significant amount of documentation in this assignment that you must read; you are better of starting it sooner rather than later.<br/>
-Global variables are not allowed and you must use prototypes <br/>
-Name files exactly as described in the documentation below.<br/> 
-All functions should match the assignment descriptions. Do not add parameters, change names, or return different values. <br/> 
-All output should match exactly what is in this document (including spacing!). If it does not match, it will not pass the autograder.<br/> 
-When part 1 is done, open a terminal and cd to your github repo, wherever you saved it. Do the following: _git add ._ then _git commit -m `<whatevermessageyouwant`>_ then _git push_.<br/>
-All work should be done on a machine where you have sudoer permission. <br/>
-All work should be your own. <br/>



**<p align = "center"> Part 1, the Process API</p>**
 **Background** <br/>
 Normally, when you log in, the OS will create a user process that binds to the login port; this causes the user process at that port to execute a shell. A shell (command line interpreter) allows the user to interact with the OS and the OS to respond to the user. The shell is a character-oriented interface that allows users to type characters terminated by Enter (the \n char). The OS will respond by sending characters back to the screen. If the OS is using a GUI, the window manager software will take over any shell tasks, and the user can access them by using a screen display with a fixed number of characters and lines. We commonly call this display your terminal, shell, or console, and in Linux, it will output a prompt, which is usually your user@machineName followed by the terminal’s current place in the file system and then a $ (see Figure 2).  

 

Common commands in Linux use bash, and usually take on the form of<br/>

command argument1 ... argumentN

For example, in
_chmod u+x `<filename`>_

_chmod_ is the command, _u+x _is an argument and `<filename`> is an argument. Not all commands require arguments- for example, you can run ls with and without any arguments. After entering a command at the prompt, the shell creates a child process to execute whatever command you provided. The following are the steps that the shell must take to be functional: 

1) Print a prompt and wait for input. <br/>
2) Get the command line input.<br/>
3) Parse the command line input.<br/>
4) Find associated files.<br/>
5) Pass any parameters from the shell to the OS command function.<br/>
6) Execute the command (with applicable parameters).<br/>

**General Directions** <br/>
Name your program _systemCaller.c_ . You will turn in the C code. **Failure to do so will result in a 0 on this portion.** In this part of the assignment, you will write a function called _executeCommand_ in the **C language**. We will use the execvp system call to launch processes when possible. However, the exit and cd (change directories) commands are not executed by execvp- they have their own system calls.  This program should consist of, at minimum, 4 functions: _main_, _executeCommand_, _changeDirectories_, and _parseInput_ (which is provided to you below). For each function, the name, return type, parameters, edge cases and exceptions that you must address, and description of functionality are provided. You may implement additional functions as you see fit. In other words, I'm asking you to write a very stripped down shell that uses a very stripped down [process API](https://www.section.io/engineering-education/fork-in-c-programming-language/).<br/>


Generally speaking, the program will execute a shell and loop until the user chooses to exit (you've seen a very basic code example of this in lecture). This shell will be interactive- that is, you will run the program (_./`<exename`>_) to launch a new shell (just like if you had opened a terminal). Then you should be able to type in various execvp launchable commands (such as _ls -la_ or _clear_), _exit_, or _cd_ into the shell, and have it perform the associated behavior. 

You may only use the following libraries, and not all of them are necessary: <br/>
 ```
<stdio.h> 
<string.h> 
<stdlib.h> 
<sys/wait.h> 
<sys/types.h> 
<unistd.h> 
<fcntl.h> 
<errno.h> 
<sys/stat.h> 
```

Any necessary display can be done using the [write()](https://man7.org/linux/man-pages/man2/write.2.html) command or the [printf()](https://man7.org/linux/man-pages/man3/printf.3.html) command. Any reading can be done using [fgets()](https://www.tutorialspoint.com/c_standard_library/c_function_fgets.htm) and/or [scanf()](https://man7.org/linux/man-pages/man3/scanf.3.html) from the C library. The man pages for any appropriate system commands/c specific commands are provided  throughout these instructions. Note that if you are asked to use a specific command (like execvp), then you must use that command- not any alternatives.  Because I assume you know how character arrays in C work, I provide the parseInput() method for every student to use to parse input entered by the user, which you can copy/paste into your code. It takes any character array, checks that there are contents in it, then fills the splitWords 2d char array with each argument. It returns the number of arguments that were parsed for use elsewhere. It will be used in executeCommand().

<code>
int parseInput(char *input, char *splitWords[]){
      int wordInd = 0;
      splitWords[0] = strtok(input, " \n");
      while(splitWords[wordInd] != NULL){
              splitWords[++wordInd] = strtok(NULL, " \n");
      }

      return wordInd;
}
</code>

Note that when [strtok](https://www.tutorialspoint.com/c_standard_library/c_function_strtok.htm) is used, and you have 2d array of tokens (see parseInput), you can access the first token and it's arguments. So if the user enters ls -la then splitWords array would look like:

ls 
-la


Where the pointer to the ls command is at splitWords[0], while the arguments(-la) are at splitWords[1]. The char array pointer can be incremented to iterate from the first command/argument combo (if necessary, which isn't the case for this iteration of the shell, but we use the 2d array here to make implementation later easier). If you do not like my parse implementation, you may write your own.

_main_ <br/>
**Input Parameters**: none<br/>
**Returned Output**: int <br/>
**Functionality**: The main function is responsible for generating the shell and looping until a user chooses to exit. It should display _exampleShell`<netid`>$ _ (where you replace `<netid`> with your netid). Pass the user input in to parseInput, and fill the passed in 2d array with the arguments entered by the user. Add  NULL as the last string in the array so that execvp executes correctly. Check the first argument of the filled array. If it is anything other than cd or exit, you should call _executeCommand_ and pass it the newly filled 2d array. If it is cd, changeDirectories should be called with appropriate arguments. If it is exit, stop looping and return from main. The return from executeCommand function should be stored as an int, and used to determine if the call was successful (1 or -1 are usually failure in Unix). You can use [strcmp](https://www.cplusplus.com/reference/cstring/strcmp/) to check the arguments entered by the user in your shell.<br/>
 

_executeCommand_<br/>
**Input Parameters**: char*[] <br/>
**Returned Output**: int <br/>
**Functionality**: executeCommand uses [execvp](https://linux.die.net/man/3/execvp) to execute a provided command as a process.  <br/>
This function should iterate through each provided argument, and fork a child process for each provided argument.
This function should [fork](https://linux.die.net/man/3/fork) a child process for the provided argument.
The fork should be checked to see if the child process was successfully created (see below). 
Then [execvp](https://linux.die.net/man/3/execvp) should be provided the command from the user that was passed into the funciton (_ls_) and any associated arguments (_ls -la_).
See General Directions if you don't know what portion of the char** array is the argument and what is the command.
The return from [execvp](https://linux.die.net/man/3/execvp) should be stored to check for errors. 
Finally, after checking for errors, [wait](https://linux.die.net/man/3/wait) should be used to wait for the process executed by [execvp](https://linux.die.net/man/3/execvp) to finish before the parent process can move on.
If the process successfully executes and forks without error, return 0. Otherwise return 1. <br/>

**Edge Cases:** If a process is not successfully forked, your function should print _fork failed!_

Hint: execvp returns -1 if it wasn't successful. <br/>

 _changeDirectories_<br/>
 **Input Parameters**: char* <br/>
 **Returned Output**: None <br/>
 **Functionality**: execvp does not execute the change directories (cd) command. To implement this functionality, you will need to write your own changeDirectories function using [chdir](https://man7.org/linux/man-pages/man2/chdir.2.html). Chdir should accept the path supplied as an input parameter. If successful, the directory location should change. Otherwise, output _Path Not Found!_<br/>
 **Edge Cases:**  Normally, if you enter cd without any path in a linux environment, the shell will change directories to the home directory. For this exercise, you do not need to have the shell do this. Instead, you should check the number of provided arguments, and if you have cd but no path, or too many trailing arguments, you should display _Path Not Found!_.<br/>
 
 
 **To Submit**<br/>
 When you are done, you should use git to git push the following to your assignment repo (see instructions above):
 1) _systemCaller.c_

You can submit as many times as you would like.
