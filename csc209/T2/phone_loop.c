#include <stdio.h>
#include <stdlib.h>

/*
 * $ gcc -Wall -std=gnu99 -g -o phone_loop phone_loop.c
 */
int main(int argc, char **argv) {
    char phone[11];
    int num = 0;
    int retval = 0;

    scanf("%10s", phone);
    while (scanf("%d", &num) == 1) {
       if (num == -1) {
          printf("%s\n", phone);
          continue;
       }
       if (num > 9 || num < -1) {
          printf("ERROR\n"); 
          retval = 1;
          continue;
       }
       printf("%c\n", phone[num]);
    }
    return retval;
}
