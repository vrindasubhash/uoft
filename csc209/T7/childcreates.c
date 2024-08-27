#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>


int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: forkloop <iterations>\n");
        exit(1);
    }

    int iterations = strtol(argv[1], NULL, 10);

    printf("%d -> ",getpid());
    for (int i = 0; i < iterations; i++) {
        fflush(stdout);
        int n = fork();
        if (n < 0) {
            perror("fork");
            exit(1);
        }
        if (n != 0) {
            return 0;
        }
        if (i == iterations - 1) {
            printf("%d\n", getpid());
            return 0;
        }
        else {
            printf("%d -> ",getpid());
        }
    }

    return 0;
}
