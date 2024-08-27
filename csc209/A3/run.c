/*****************************************************************************/
/*                           CSC209-24s A3 CSCSHELL                          */
/*       Copyright 2024 -- Demetres Kostas PhD (aka Darlene Heliokinde)      */
/*****************************************************************************/

#include "cscshell.h"
//#define DEBUG 1
//@vrinda


// COMPLETE
int cd_cscshell(const char *target_dir){
    if (target_dir == NULL) {
        char user_buff[MAX_USER_BUF];
        if (getlogin_r(user_buff, MAX_USER_BUF) != 0) {
           perror("run_command");
           return -1;
        }
        struct passwd *pw_data = getpwnam((char *)user_buff);
        if (pw_data == NULL) {
           perror("run_command");
           return -1;
        }
        target_dir = pw_data->pw_dir;
    }

    if(chdir(target_dir) < 0){
        perror("cd_cscshell");
        return -1;
    }
    return 0;
}


int *execute_line(Command *head){
    #ifdef DEBUG
    printf("\n***********************\n");
    printf("BEGIN: Executing line...\n");
    #endif

    run_command(head);

    #ifdef DEBUG
    printf("All children created\n");
    #endif

    // Wait for all the children to finish
    int status = 0;
    wait(&status);
 
    #ifdef DEBUG
    printf("All children finished\n");
    #endif

    #ifdef DEBUG
    printf("END: Executing line...\n");
    printf("***********************\n\n");
    #endif
    int * ret = safe_malloc(sizeof(int));
    *ret = WEXITSTATUS(status); 

    return ret;
}


/*
** Forks a new process and execs the command
** making sure all file descriptors are set up correctly.
**
** Parent process returns -1 on error.
** Any child processes should not return.
*/
int run_command(Command *command){
    #ifdef DEBUG
    printf("Running command: %s\n", command->exec_path);
    printf("Argvs: ");
    if (command->args == NULL){
        printf("NULL\n");
    }
    else if (command->args[0] == NULL){
        printf("Empty\n");
    }
    else {
        for (int i=0; command->args[i] != NULL; i++){
            printf("%d: [%s] ", i+1, command->args[i]);
        }
    }
    printf("\n");
    printf("Redir out: %s\n Redir in: %s\n",
           command->redir_out_path, command->redir_in_path);
    printf("Stdin fd: %d | Stdout fd: %d\n",
           command->stdin_fd, command->stdout_fd);
    #endif
    
    if (strcmp(command->exec_path, CD) == 0) 
       return cd_cscshell(command->args[1]);

    // fork and exec
    int pid = fork();
    if (pid == -1) {
        perror("fork");
        return -1;
    }
    if (pid == 0) {
        execv(command->exec_path, command->args);
        perror("execv"); // should never reach here if execv succeeds
        return -1;
    }


    #ifdef DEBUG
    printf("Parent process created child PID [%d] for %s\n", pid, command->exec_path);
    #endif
    return 0;
}


int run_script(char *file_path, Variable **root){
    FILE *f = fopen(file_path, "r"); 
    if (f == NULL) {
        ERR_PRINT("Unable to open file %s\n", file_path);
        return -1;
    }
    
    char buffer[MAX_SINGLE_LINE + 1];
   
    int i = 0; 
    while (fgets(buffer, MAX_SINGLE_LINE, f) != NULL) {
        buffer[MAX_SINGLE_LINE] = '\0';        
        if (buffer[strlen(buffer) - 1] == '\n') 
            buffer[strlen(buffer) - 1] = '\0';
        Command * cmd = parse_line(buffer, root);  

        free_command(cmd);
        i++;
    }

    fclose(f);
    return 0;
}

void free_command(Command *command){
    while (command != NULL) {
        Command * tmp = command;
        command = command->next;
        SAFE_FREE(tmp->exec_path);
        SAFE_FREE(tmp->redir_in_path);
        SAFE_FREE(tmp->redir_out_path);
        if (tmp->args != NULL) {
            for (int i=0; tmp->args[i] != NULL; i++){
                free(tmp->args[i]);
            }
            free(tmp->args);
        }
        free(tmp);
    }
}
