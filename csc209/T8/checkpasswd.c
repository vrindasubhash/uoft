#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAXLINE 256
#define MAX_PASSWORD 10  

#define SUCCESS "Password verified\n"
#define INVALID "Invalid password\n"
#define NO_USER "No such user\n"

int main(void) {
  char user_id[MAXLINE];
  char password[MAXLINE];

  pid_t pid = 0;
  int status = 0;
  int pipefd[2]; 

  /* The user will type in a user name on one line followed by a password 
     on the next.
     DO NOT add any prompts.  The only output of this program will be one 
	 of the messages defined above.
     Please read the comments in validate carefully
   */

  if(fgets(user_id, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }
  if(fgets(password, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }
  
  user_id[MAXLINE - 1] = '\0';
  password[MAXLINE - 1] = '\0'; 
  
  if (pipe(pipefd) == -1) {
    perror("pipefd");
    exit(1);
  }

  pid = fork();

  if (pid == 0) {
    // child

    close(pipefd[1]);

    dup2(pipefd[0], STDIN_FILENO);

    close(pipefd[0]);

    execlp("./validate", "validate", NULL);
    perror("execlp failed");
    exit(1);

  } else if (pid > 0) {
    // parent

    close(pipefd[0]);
    
    if (write(pipefd[1], user_id, MAX_PASSWORD) == -1) {
      perror("write");
      exit(1);
    }

    if (write(pipefd[1], password, MAX_PASSWORD) == -1) {
      perror("write");
      exit(1);
    }
  
    close(pipefd[1]);

    if (wait(&status) == -1) {
      perror("wait error");
      exit(1);
    } else {
      if (WIFEXITED(status) == 0)
        exit(-1);
      status = WEXITSTATUS(status);
      if (status == 0) {
        printf(SUCCESS);
      }
      if (status == 2) {
        printf(INVALID);
      }
      if (status == 3) {
        printf(NO_USER);
      }
    }
  } else {
    // failed
    perror("fork failed");
    exit(1);
  }

  return 0;
}
