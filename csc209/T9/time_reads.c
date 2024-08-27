/* The purpose of this program is to practice writing signal handling
 * functions and observing the behaviour of signals.
 */

#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <string.h>

/* Message to print in the signal handling function. */
#define MESSAGE "%ld reads were done in %ld seconds.\n"

/* Global variables to store number of read operations and seconds elapsed. 
 */
long num_reads, seconds;


void signal_handler(int signum) {
    printf(MESSAGE, num_reads, seconds);
    exit(0); 
}

void time_handler(int signum) {
    printf(MESSAGE, num_reads, seconds);
    exit(0); 
}

/* The first command-line argument is the number of seconds to set a timer to run.
 * The second argument is the name of a binary file containing 100 ints.
 * Assume both of these arguments are correct.
 */

int main(int argc, char **argv) {
    num_reads = 0;
    if (argc != 3) {
      fprintf(stderr, "Usage: time_reads s filename\n");
      exit(1);
    }
    seconds = strtol(argv[1], NULL, 10);

    FILE *fp;
    if ((fp = fopen(argv[2], "rb")) == NULL) {
      perror("fopen");
      exit(1);
    }
   
    struct sigaction act;
    memset(&act, 0, sizeof(act));

    sigemptyset(&act.sa_mask);
    act.sa_flags = 0;

    // Set the handler function
    act.sa_handler = signal_handler;

    // Register the signal handler for SIGINT
    if (sigaction(SIGPROF, &act, NULL) < 0) {
      perror("sigaction");
      exit(1);
    }


    struct itimerval timer;
    memset(&timer, 0, sizeof(timer));
    timer.it_value.tv_sec = seconds;

    if (signal(SIGALRM, time_handler) == SIG_ERR) {
      perror("signal");
      exit(1);
    }

    if (setitimer(ITIMER_REAL, &timer, NULL) == -1) {
        perror("timer");
        exit(1);
    }

    /* In an infinite loop, read an int from a random location in the file,
     * and print it to stderr.
     */
    for (;;) {
      int randomIdx = rand() % 100;
      fseek(fp, randomIdx * sizeof(int), SEEK_SET);
      int number;
      fread(&number, sizeof(int), 1, fp);
      num_reads++;
      fprintf(stderr,"%d\n", number);
    }

    return 1; // something is wrong if we ever get here!
}
